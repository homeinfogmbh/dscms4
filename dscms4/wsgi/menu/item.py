"""DSCMS4 WSGI handlers for menu items."""

from itertools import chain

from flask import request

from his import CUSTOMER, JSON_DATA, authenticated, authorized
from wsgilib import JSON

from dscms4.messages.menu import NoSuchMenuItem, MenuItemAdded, \
    MenuItemPatched, MenuItemDeleted, MenuItemsSorted, DifferentMenusError, \
    DifferentParentsError
from dscms4.orm.menu import Menu, MenuItem
from dscms4.wsgi.menu.menu import get_menu


__all__ = ['ROUTES', 'get_menu_item']


def get_menu_item(ident):
    """Returns the respective menu item."""

    try:
        return MenuItem.select().join(Menu).where(
            (Menu.customer == CUSTOMER.id) & (MenuItem.id == ident)).get()
    except MenuItem.DoesNotExist:
        raise NoSuchMenuItem()


@authenticated
@authorized('dscms4')
def list_(menu):
    """Lists the respective menu's items."""

    menu = get_menu(menu)
    return JSON([
        menu_item.to_json() for menu_item in MenuItem.select().where(
            MenuItem.menu == menu)])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective menu item."""

    charts = 'charts' in request.args
    children = 'children' in request.args
    menu_item = get_menu_item(ident)
    return JSON(menu_item.to_json(charts=charts, children=children))


@authenticated
@authorized('dscms4')
def add():
    """Adds a new menu item."""

    menu_item = MenuItem.from_json(JSON_DATA, CUSTOMER.id)
    menu_item.save()
    return MenuItemAdded(id=menu_item.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches a new menu item."""

    menu_item = get_menu_item(ident)
    menu_item.patch_json(JSON_DATA)
    menu_item.save()
    return MenuItemPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes a menu or menu item."""

    update_children = 'updateChildren' in request.args
    menu_item = get_menu_item(ident)
    menu_item.delete_instance(update_children=update_children)
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
