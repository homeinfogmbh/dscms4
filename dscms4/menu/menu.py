"""DSCMS4 WSGI handlers for menus."""

from flask import request

from cmslib.functions.menu import get_menu
from cmslib.messages.menu import INVALID_MENU_DATA
from cmslib.messages.menu import MENU_ADDED
from cmslib.messages.menu import MENU_COPIED
from cmslib.messages.menu import MENU_DELETED
from cmslib.messages.menu import MENU_PATCHED
from cmslib.orm.menu import Menu
from his import CUSTOMER, JSON_DATA, authenticated, authorized
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """List menus."""

    menus = Menu.select().where(Menu.customer == CUSTOMER.id)
    items = 'items' in request.args

    if 'assoc' in request.args:
        json = {
            menu.id: menu.to_json(skip=('id',), items=items) for menu in menus
        }
        return JSON(json)

    return JSON([menu.to_json(items=items) for menu in menus])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the respective menu."""

    menu = get_menu(ident)
    items = 'items' in request.args
    return JSON(menu.to_json(items=items))


@authenticated
@authorized('dscms4')
def add() -> JSONMessage:
    """Adds a new menu."""

    try:
        menu = Menu.from_json(JSON_DATA)
    except ValueError:
        return INVALID_MENU_DATA

    menu.save()
    return MENU_ADDED.update(id=menu.id)


@authenticated
@authorized('dscms4')
def patch(ident: int) -> JSONMessage:
    """Patches the respective menu."""

    menu = get_menu(ident)

    try:
        menu.patch_json(JSON_DATA)
    except ValueError:
        return INVALID_MENU_DATA

    menu.save()
    return MENU_PATCHED


@authenticated
@authorized('dscms4')
def copy(ident: int) -> JSONMessage:
    """Copies the respective menu."""

    menu = get_menu(ident)
    copy, *records = menu.copy()    # pylint: disable=W0621
    copy.save()

    for record in records:
        record.save()

    return MENU_COPIED.update(id=copy.id)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes a menu."""

    menu = get_menu(ident)
    menu.delete_instance()
    return MENU_DELETED


ROUTES = (
    ('GET', '/menu', list_),
    ('GET', '/menu/<int:ident>', get),
    ('POST', '/menu', add),
    ('PATCH', '/menu/<int:ident>', patch),
    (('COPY', 'PUT'), '/menu/<int:ident>', copy),
    ('DELETE', '/menu/<int:ident>', delete)
)
