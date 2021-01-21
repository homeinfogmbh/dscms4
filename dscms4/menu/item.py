"""DSCMS4 WSGI handlers for menu items."""

from itertools import chain

from flask import request

from cmslib.functions.menu import get_menu_item, get_menu_items
from cmslib.orm.menu import MenuItem
from his import CUSTOMER, authenticated, authorized, require_json
from wsgilib import JSON, JSONMessage, get_bool, get_int


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists the respective menu's items."""

    return JSON([record.to_json() for record in get_menu_items(
        menu=get_int('menu'))])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the respective menu item."""

    return JSON(get_menu_item(ident).to_json(
        charts=get_bool('charts'), children=get_bool('children')))


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds a new menu item."""

    record = MenuItem.from_json(request.json, CUSTOMER.id)
    record.save()
    return JSONMessage('Menu item added.', id=record.id, status=201)


@authenticated
@authorized('dscms4')
@require_json(dict)
def patch(ident: int) -> JSONMessage:
    """Patches a new menu item."""

    menu_item = get_menu_item(ident)
    record = menu_item.patch_json(request.json)
    record.save()
    return JSONMessage('Menu item patched.', status=200)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes a menu or menu item."""

    record = get_menu_item(ident)
    record.delete_instance(update_children=get_bool('updateChildren'))
    return JSONMessage('Menu item delted.', status=200)


@authenticated
@authorized('dscms4')
@require_json(list)
def order() -> JSONMessage:
    """Orders the respective menu items."""

    try:
        first, *other = map(get_menu_item, request.json)
    except ValueError:
        return JSONMessage('No items to sort.', status=200)

    if not all(menu_item.menu == first.menu for menu_item in other):
        return JSONMessage('Items belong to different menus.', status=400)

    if not all(menu_item.parent == first.parent for menu_item in other):
        return JSONMessage('Items have different parents.', status=400)

    for index, record in enumerate(chain((first,), other)):
        record.index = index
        record.save()

    return JSONMessage('Menu items sorted.', status=200)


ROUTES = (
    ('GET', '/menu/<int:menu>/items', list_),
    ('GET', '/menu/item/<int:ident>', get),
    ('POST', '/menu/item', add),
    ('PATCH', '/menu/item/<int:ident>', patch),
    ('DELETE', '/menu/item/<int:ident>', delete),
    ('POST', '/menu/item/order', order)
)
