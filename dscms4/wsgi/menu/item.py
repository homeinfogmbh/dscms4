"""DSCMS4 WSGI handlers for menu items."""

from itertools import chain

from flask import request

from his import JSON_DATA, authenticated, authorized
from wsgilib import JSON

from dscms4.messages.menu import NoSuchMenu, InvalidMenuData, NoSuchMenuItem, \
    MenuItemAdded, MenuItemPatched, MenuItemDeleted, MenuItemsSorted, \
    DifferentMenusError, DifferentParentsError
from dscms4.orm.menu import Menu, MenuItem


__all__ = ['ROUTES']


def get_menu_item(ident):
    """Returns the respective menu item."""

    menus = Menu.cselect().where(True)

    try:
        return MenuItem.cget((MenuItem.id == ident) & (MenuItem.menu << menus))
    except MenuItem.DoesNotExist:
        raise NoSuchMenuItem()


@authenticated
@authorized('dscms4')
def list_(menu):
    """Lists the respective menu's items."""

    try:
        menu = Menu.cget(Menu.id == menu)
    except Menu.DoesNotExist:
        return NoSuchMenu()

    return JSON([
        menu_item.to_json() for menu_item in MenuItem.cselect().where(
            MenuItem.menu == menu)])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective menu item."""

    charts = 'charts' in request.args
    children = 'children' in request.args
    return JSON(get_menu_item(ident).to_json(cahrts=charts, children=children))


@authenticated
@authorized('dscms4')
def add():
    """Adds a new menu item."""

    try:
        menu_item = MenuItem.from_json(JSON_DATA)
    except ValueError as value_error:
        return InvalidMenuData(error=str(value_error))

    menu_item.save()
    return MenuItemAdded(id=menu_item.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches a new menu item."""

    menu_item = get_menu_item(ident)

    try:
        menu_item.patch_json(JSON_DATA)
    except ValueError as value_error:
        return InvalidMenuData(error=str(value_error))

    menu_item.save()
    return MenuItemPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes a menu or menu item."""

    update_children = 'updateChildren' in request.args
    get_menu_item(ident).delete_instance(update_children=update_children)
    return MenuItemDeleted()


@authenticated
@authorized('dscms4')
def order():
    """Orders the respective menu items."""

    menu_items = (get_menu_item(ident) for ident in JSON_DATA)

    try:
        first, *other = menu_items
    except ValueError:
        return MenuItemsSorted()    # Empty set of MenuItems.

    if not all(menu_item.menu == first.menu for menu_item in other):
        return DifferentMenusError()

    if not all(menu_item.parent == first.parent for menu_item in other):
        return DifferentParentsError()

    for index, menu_item in enumerate(chain((first,), other)):
        menu_item.index = index
        menu_item.save()

    return MenuItemsSorted()


ROUTES = (
    ('GET', '/menu/<int:menu>/items', list_, 'list_menu_items'),
    ('GET', '/menu/item/<int:ident>', get, 'get_menu_item'),
    ('POST', '/menu/item', add, 'add_menu_item'),
    ('PATCH', '/menu/item/<int:ident>', patch, 'patch_menu_item'),
    ('DELETE', '/menu/item/<int:ident>', delete, 'delete_menu_item'),
    ('POST', '/menu/item/order', order, 'order_menu_items'))
