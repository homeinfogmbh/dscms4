"""DSCMS4 WSGI handlers for menu items."""

from his import CUSTOMER, DATA, authenticated, authorized
from wsgilib import JSON

from dscms4.messages.charts import NoSuchChart
from dscms4.messages.menu import InvalidMenuData, NoSuchMenuItem, \
    MenuItemAdded, MenuItemPatched, MenuItemDeleted
from dscms4.orm.charts import BaseChart
from dscms4.orm.menu import UNCHANGED, MenuItem
from dscms4.wsgi.menu.menu import get_menu

__all__ = ['ROUTES']


def get_menu_items(menu):
    """Yields menus of the current customer."""

    return MenuItem.select().where(MenuItem.menu == menu)


def get_menu_item(menu, ident):
    """Returns the respective menu item."""

    try:
        return MenuItem.get((MenuItem.menu == menu) & (MenuItem.id == ident))
    except MenuItem.DoesNotExist:
        raise NoSuchMenuItem()


def parent_menu_item(menu, dictionary):
    """Returns the respective parent menu item."""

    try:
        parent = dictionary.pop('parent')
    except KeyError:
        return None

    try:
        return MenuItem.get(
            (MenuItem.menu == menu) & (MenuItem.parent == parent))
    except MenuItem.DoesNotExist:
        raise NoSuchMenuItem()


def get_chart(ident):
    """Returns the respective chart for the menu item."""

    try:
        return BaseChart.get(
            (BaseChart.customer == CUSTOMER.id) & (BaseChart.id == ident))
    except BaseChart.DoesNotExist:
        raise NoSuchChart()


@authenticated
@authorized('dscms4')
def list_(menu_id):
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
    parent = parent_menu_item(menu, json)

    try:
        chart_id = json.pop('chart')
    except KeyError:
        chart = None
    else:
        chart = get_chart(chart_id)

    try:
        menu_item = MenuItem.from_dict(menu, json, parent=parent, chart=chart)
    except ValueError:
        raise InvalidMenuData()

    menu_item.save()
    return MenuItemAdded(id=menu_item.id)


@authenticated
@authorized('dscms4')
def patch(menu_id, item_id):
    """Patches a new menu item."""

    menu = get_menu(menu_id)
    menu_item = get_menu_item(menu, item_id)
    json = DATA.json

    try:
        menu_id = json.pop('menu')
    except KeyError:
        new_menu = UNCHANGED
    else:
        new_menu = get_menu(menu_id)

    try:
        parent_id = json.pop('menu')
    except KeyError:
        new_parent = UNCHANGED
    else:
        new_parent = get_menu_item(new_menu or menu, parent_id)

    try:
        chart_id = json.pop('chart')
    except KeyError:
        new_chart = UNCHANGED
    else:
        new_chart = get_chart(chart_id)

    try:
        menu_item.patch(new_menu, new_parent, new_chart, json)
    except ValueError:
        raise InvalidMenuData()

    menu_item.save()
    return MenuItemPatched()


@authenticated
@authorized('dscms4')
def delete(menu_id, item_id):
    """Deletes a menu or menu item."""

    get_menu_item(get_menu(menu_id), item_id).delete_instance()
    return MenuItemDeleted()


ROUTES = (
    ('GET', '/menu/<int:menu_id>/item', list_, 'list_menu_items'),
    ('GET', '/menu/<int:menu_id>/item/<int:item_id>', get, 'get_menu_item'),
    ('POST', '/menu/<int:menu_id>/item', add, 'add_menu_item'),
    ('PATCH', '/menu/<int:menu_id>/item/<int:item_id>', patch,
     'patch_menu_item'),
    ('DELETE', '/menu/<int:menu_id>/item/<int:item_id>', delete,
     'delete_menu_item'))
