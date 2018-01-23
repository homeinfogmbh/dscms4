"""Menu item controllers."""

from peewee import DoesNotExist

from his import CUSTOMER, DATA, authenticated, authorized
from wsgilib import JSON

from dscms4.messages.charts import NoSuchChart
from dscms4.messages.menu import InvalidMenuData, NoSuchMenuItem, \
    MenuItemAdded, MenuItemDeleted
from dscms4.orm.charts import BaseChart
from dscms4.orm.menu import MenuItem
from dscms4.wsgi.menu.menu import get_menu

__all__ = ['ROUTES']


def get_menu_items(menu):
    """Yields menus of the current customer."""

    return MenuItem.select().where(MenuItem.menu == menu)


def get_menu_item(menu, ident):
    """Returns the respective menu item."""

    try:
        return MenuItem.get((MenuItem.menu == menu) & (MenuItem.id == ident))
    except DoesNotExist:
        raise NoSuchMenuItem()


def parent_menu_item(menu, dictionary):
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


def menu_item_chart(dictionary):
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


@authenticated
@authorized('dscms4')
def lst(menu_id):
    """Lists the respective menu's items."""

    return JSON([
        menu_item.to_dict() for menu_item in
        get_menu_items(get_menu(menu_id))])


@authenticated
@authorized('dscms4')
def get(menu_id, item_id):
    """Returns the respective menu item."""

    return JSON(get_menu_item(get_menu(menu_id), item_id).to_dict())


@authenticated
@authorized('dscms4')
def add(menu_id):
    """Adds a new menu item."""

    menu = get_menu(menu_id)
    json = DATA.json

    try:
        menu_item = MenuItem.from_dict(
            json, menu=menu, parent=parent_menu_item(menu, json),
            chart=menu_item_chart(json))
    except ValueError:
        raise InvalidMenuData()

    menu_item.save()
    return MenuItemAdded(id=menu_item.id)


@authenticated
@authorized('dscms4')
def delete(menu_id, item_id):
    """Deletes a menu or menu item."""

    get_menu_item(get_menu(menu_id), item_id).delete_instance()
    return MenuItemDeleted()


ROUTES = (
    ('GET', '/menu/<int:menu_id>/item', lst, 'list_menu_items'),
    ('GET', '/menu/<int:menu_id>/item/<int:item_id>', get, 'get_menu_item'),
    ('POST', '/menu/<int:menu_id>/item', add, 'add_menu_item'),
    ('DELETE', '/menu/<int:menu_id>/item/<int:item_id>', delete,
     'delete_menu_item'))
