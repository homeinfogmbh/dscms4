"""DSCMS4 WSGI handlers for menus."""

from flask import request

from cmslib.functions.menu import get_menu, get_menus
from cmslib.orm.menu import Menu
from his import authenticated, authorized, require_json
from wsgilib import JSON, JSONMessage, get_bool


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """List menus."""

    items = get_bool('items')

    if get_bool('assoc'):
        return JSON({
            menu.id: menu.to_json(skip={'id'}, items=items)
            for menu in get_menus()
        })

    return JSON([menu.to_json(items=items) for menu in get_menus()])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the respective menu."""

    return JSON(get_menu(ident).to_json(items=get_bool('items')))


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

    menu = get_menu(ident)
    menu.patch_json(request.json)
    menu.save()
    return JSONMessage('Menu patched.', status=200)


@authenticated
@authorized('dscms4')
def copy_(ident: int) -> JSONMessage:
    """Copies the respective menu."""

    menu = get_menu(ident)
    copy, *records = menu.copy()
    copy.save()

    for record in records:
        record.save()

    return JSONMessage('Menu copied.', id=copy.id, status=200)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes a menu."""

    get_menu(ident).delete_instance()
    return JSONMessage('Menu deleted.', status=200)


ROUTES = [
    ('GET', '/menu', list_),
    ('GET', '/menu/<int:ident>', get),
    ('POST', '/menu', add),
    ('PATCH', '/menu/<int:ident>', patch),
    (('COPY', 'PUT'), '/menu/<int:ident>', copy_),
    ('DELETE', '/menu/<int:ident>', delete)
]
