"""DSCMS4 WSGI handlers for menu items."""

from itertools import chain

from flask import request

from cmslib.functions.menu import get_menu, get_menu_item
from cmslib.messages.menu import DIFFERENT_MENUS
from cmslib.messages.menu import DIFFERENT_PARENTS
from cmslib.messages.menu import MENU_ITEM_ADDED
from cmslib.messages.menu import MENU_ITEM_DELETED
from cmslib.messages.menu import MENU_ITEM_PATCHED
from cmslib.messages.menu import MENU_ITEMS_SORTED
from cmslib.orm.menu import MenuItem
from his import CUSTOMER, JSON_DATA, authenticated, authorized
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_(menu: int) -> JSON:
    """Lists the respective menu's items."""

    menu = get_menu(menu)
    return JSON([
        menu_item.to_json() for menu_item in MenuItem.select().where(
            MenuItem.menu == menu)
    ])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the respective menu item."""

    charts = 'charts' in request.args
    children = 'children' in request.args
    menu_item = get_menu_item(ident)
    return JSON(menu_item.to_json(charts=charts, children=children))


@authenticated
@authorized('dscms4')
def add() -> JSONMessage:
    """Adds a new menu item."""

    menu_item_group = MenuItem.from_json(JSON_DATA, CUSTOMER.id)
    menu_item_group.save()
    return MENU_ITEM_ADDED.update(id=menu_item_group.id)


@authenticated
@authorized('dscms4')
def patch(ident: int) -> JSONMessage:
    """Patches a new menu item."""

    menu_item = get_menu_item(ident)
    menu_item_group = menu_item.patch_json(JSON_DATA)
    menu_item_group.save()
    return MENU_ITEM_PATCHED


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes a menu or menu item."""

    update_children = 'updateChildren' in request.args
    menu_item = get_menu_item(ident)
    menu_item.delete_instance(update_children=update_children)
    return MENU_ITEM_DELETED


@authenticated
@authorized('dscms4')
def order() -> JSONMessage:
    """Orders the respective menu items."""

    menu_items = (get_menu_item(ident) for ident in JSON_DATA)

    try:
        first, *other = menu_items
    except ValueError:
        return MENU_ITEMS_SORTED    # Empty set of MenuItems.

    if not all(menu_item.menu == first.menu for menu_item in other):
        return DIFFERENT_MENUS

    if not all(menu_item.parent == first.parent for menu_item in other):
        return DIFFERENT_PARENTS

    for index, menu_item in enumerate(chain((first,), other)):
        menu_item.index = index
        menu_item.save()

    return MENU_ITEMS_SORTED


ROUTES = (
    ('GET', '/menu/<int:menu>/items', list_),
    ('GET', '/menu/item/<int:ident>', get),
    ('POST', '/menu/item', add),
    ('PATCH', '/menu/item/<int:ident>', patch),
    ('DELETE', '/menu/item/<int:ident>', delete),
    ('POST', '/menu/item/order', order)
)
