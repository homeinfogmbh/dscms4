"""DSCMS4 WSGI handlers for menus."""

from peewee import DoesNotExist

from his import CUSTOMER, DATA

from dscms4.messages.chart import NoSuchChart
from dscms4.messages.menu import NoMenuSpecified, NoSuchMenu, InvalidMenuData,\
    MenuAdded, MenuDeleted, NoMenuItemSpecified, NoSuchMenuItem, \
    MenuItemAdded, MenuItemDeleted
from dscms4.orm.charts import BaseChart
from dscms4.orm.exceptions import NoSuchChart
from dscms4.orm.menu import Menu, MenuItem

__all__ = ['ROUTES']


def _get_menu(ident):
    """Returns the respective menu by its ID."""

    try:
        return Menu.get((Menu.customer == CUSTOMER.id) & (Menu.id == ident))
    except DoesNotExist:
        raise NoSuchMenu()


def _get_menus():
    """Yields the menus of the current customer."""

    return Menu.select().where(Menu.customer == self.customer)


MENUS = LocalProxy(_get_menus)


def _get_menu_items(menu):
    """Yields menus of the current customer."""

    return MenuItem.select().where(MenuItem.menu == menu)


def _get_menu_item(menu, ident):
    """Returns the respective menu item."""

    try:
        return MenuItem.get((MenuItem.menu == menu) & (MenuItem.id == ident))
    except DoesNotExist:
        raise NoSuchMenuItem()


def _parent_menu_item(menu, dictionary):
    """Returns the respective parent menu item."""

    parent = dictionary.get('parent')

    if parent is None:
        return None

    parent = int(parent)

    try:
        return MenuItem.get(
            (MenuItem.menu == menu) & (MenuItem.parent == parent))
    except DoesNotExist:
        raise NoSuchMenuItem()


def _menu_item_chart(dictionary):
    """Returns the respective chart for the menu item."""

    chart = dictionary.get('chart')

    if chart is None:
        return None

    chart = int(chart)

    try:
        return BaseChart.get(
            (BaseChart.customer == CUSTOMER.id) & (BaseChart.id == chart))
    except DoesNotExist:
        raise NoSuchChart()


def lst():
    """List menus."""

    return JSON([menu.to_dict() for menu in MENUS])


def get(ident):
    """Returns the respective menu."""

    return JSON(_get_menu(ident).to_dict())


def add():
    """Adds a new menu."""

    try:
        menu = Menu.from_dict(DATA.json, customer=CUSTOMER.id)
    except ValueError:
        raise InvalidMenuData()

    menu.save()
    return MenuAdded(id=menu.id)


def delete(ident):
    """Deletes a menu."""

    _get_menu(ident).delete_instance()
    return MenuDeleted()


def list_items(menu_id):
    """Lists the respective menu's items."""

    return JSON([
        menu_item.to_dict() for menu_item in
        _get_menu_items(_get_menu(menu_id))])


def get_item(menu_id, item_id):
    """Returns the respective menu item."""

    return JSON(_get_menu_item(_get_menu(menu_id), item_id).to_dict())


def add_item(menu_id):
    """Adds a new menu item."""

    menu = _get_menu(menu_id)
    json = DATA.json

    try:
        menu_item = MenuItem.from_dict(
            json, menu=menu, parent=_parent_menu_item(menu, json),
            chart=_menu_item_chart(json))
    except ValueError:
        raise InvalidMenuData()

    menu_item.save()
    return MenuItemAdded(id=menu_item.id)


def delete(menu_id, item_id):
    """Deletes a menu or menu item."""

    _get_menu_item(_get_menu(menu_id), item_id).delete_instance()
    return MenuItemDeleted()


ROUTES = (
    ('GET', '/menu', lst, 'list_menu'),
    ('GET', '/menu/<int:ident>', get, 'get_menu'),
    ('POST', '/menu', add, 'add_menu'),
    ('DELETE', '/menu/<int:ident>', delete, 'delete_menu'),
    ('GET', '/menu/<int:menu_id>/item', list_items, 'list_items'),
    ('GET', '/menu/<int:menu_id>/item/<int:item_id>', get_item, 'get_item'),
    ('POST', '/menu/<int:menu_id>/item', add_item, 'add_item')
    ('DELETE', '/menu/<int:menu_id>/item/<int:item_id>', delete_item,
     'delete_item'))
