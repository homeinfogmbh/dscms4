"""DSCMS4 WSGI handlers for menus."""

from flask import request

from cmslib import Menu
from cmslib import MenuItem
from cmslib import MenuItemChart
from cmslib import get_menu
from cmslib import get_menus
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage, get_bool, require_json


__all__ = ['ROUTES']


def get_kwargs():
    """Returns the menu items."""

    kwargs = {}

    if get_bool('items'):
        kwargs['menu_items'] = MenuItem.select(cascade=True)
        kwargs['menu_item_charts'] = MenuItemChart.select(cascade=True)

    return kwargs


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """List menus."""

    return JSON([
        menu.to_json(**get_kwargs()) for menu in get_menus(CUSTOMER.id)
    ])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the respective menu."""

    return JSON(get_menu(ident, CUSTOMER.id).to_json(**get_kwargs()))


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds a new menu."""

    menu = Menu.from_json(request.json)
    menu.save()
    return JSONMessage('Menu added.', id=menu.id, status=201)


@authenticated
@authorized('dscms4')
@require_json(dict)
def patch(ident: int) -> JSONMessage:
    """Patches the respective menu."""

    menu = get_menu(ident, CUSTOMER.id)
    menu.patch_json(request.json)
    menu.save()
    return JSONMessage('Menu patched.', status=200)


@authenticated
@authorized('dscms4')
def copy_(ident: int) -> JSONMessage:
    """Copies the respective menu."""

    menu = get_menu(ident, CUSTOMER.id)
    copy, *records = menu.copy()
    copy.save()

    for record in records:
        record.save()

    return JSONMessage('Menu copied.', id=copy.id, status=200)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes a menu."""

    get_menu(ident, CUSTOMER.id).delete_instance()
    return JSONMessage('Menu deleted.', status=200)


ROUTES = [
    ('GET', '/menu', list_),
    ('GET', '/menu/<int:ident>', get),
    ('POST', '/menu', add),
    ('PATCH', '/menu/<int:ident>', patch),
    (('COPY', 'PUT'), '/menu/<int:ident>', copy_),
    ('DELETE', '/menu/<int:ident>', delete)
]
