"""DSCMS4 WSGI handlers for menu items."""

from his import CUSTOMER, DATA, authenticated, authorized
from his.messages import MissingData
from wsgilib import JSON

from dscms4.messages.menu import InvalidMenuData, NoSuchMenuItem, \
    MenuItemAdded, MenuItemPatched, MenuItemDeleted, MenuItemsSorted, \
    DifferentMenusError
from dscms4.orm.menu import UNCHANGED, Menu, MenuItem
from dscms4.wsgi.menu.menu import get_menu

__all__ = ['ROUTES']


def get_menu_items(menu):
    """Yields menus of the current customer."""

    return MenuItem.select().where(MenuItem.menu == menu)


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

    return JSON([
        menu_item.to_dict() for menu_item in
        get_menu_items(get_menu(menu))])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective menu item."""

    return JSON(get_menu_item(ident).to_dict())


@authenticated
@authorized('dscms4')
def add():
    """Adds a new menu item."""

    json = DATA.json

    try:
        menu = json.pop('menu')
    except KeyError:
        raise MissingData(key='menu')

    menu = get_menu(menu)
    parent = json.pop('parent', None)

    if parent is not None:
        parent = get_menu_item(parent)

    try:
        menu_item = MenuItem.from_dict(menu, json, parent=parent)
    except ValueError:
        raise InvalidMenuData()

    menu_item.save()
    return MenuItemAdded(id=menu_item.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches a new menu item."""

    menu_item = get_menu_item(ident)
    json = DATA.json

    try:
        menu = json.pop('menu')
    except KeyError:
        menu = UNCHANGED
    else:
        menu = get_menu(menu)

    try:
        parent = json.pop('parent')
    except KeyError:
        parent = UNCHANGED
    else:
        parent = get_menu_item(parent)
        common_menu = menu_item.menu if menu is UNCHANGED else menu

        if parent.menu != common_menu:
            raise DifferentMenusError()

    try:
        menu_item.patch(json, menu=menu, parent=parent)
    except ValueError:
        raise InvalidMenuData()

    menu_item.save()
    return MenuItemPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes a menu or menu item."""

    get_menu_item(ident).delete_instance()
    return MenuItemDeleted()


@authenticated
@authorized('dscms4')
def order():
    """Orders the respective menu items."""

    menu_items = tuple(get_menu_item(ident) for ident in DATA.json)

    try:
        sentinel = menu_items[0].menu
    except IndexError:
        return MenuItemsSorted()    # Empty list.

    if all(menu_item.group == sentinel for menu_item in menu_items[1:]):
        for index, menu_item in enumerate(menu_items):
            menu_item.index = index
            menu_item.save()

        return MenuItemsSorted()

    return DifferentMenusError()


ROUTES = (
    ('GET', '/menu/<int:menu>/items', list_, 'list_menu_items'),
    ('GET', '/menu/item/<int:ident>', get, 'get_menu_item'),
    ('POST', '/menu/item', add, 'add_menu_item'),
    ('PATCH', '/menu/item/<int:ident>', patch, 'patch_menu_item'),
    ('DELETE', '/menu/item/<int:ident>', delete, 'delete_menu_item'),
    ('POST', '/menu/item/order', order, 'order_menu_items'))
