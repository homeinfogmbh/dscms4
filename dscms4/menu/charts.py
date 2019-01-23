"""DSCMS4 WSGI handlers for menu item charts."""

from itertools import chain

from cmslib.messages.charts import INVALID_CHART_TYPE, NO_SUCH_CHART
from cmslib.messages.menu import DIFFERENT_MENU_ITEMS
from cmslib.messages.menu import MENU_ITEM_CHART_ADDED
from cmslib.messages.menu import MENU_ITEM_CHART_DELETED
from cmslib.messages.menu import MENU_ITEM_CHARTS_SORTED
from cmslib.messages.menu import NO_SUCH_MENU_ITEM_CHART
from cmslib.orm.charts import BaseChart, Chart
from cmslib.orm.menu import Menu, MenuItem, MenuItemChart
from his import CUSTOMER, JSON_DATA, authenticated, authorized
from his.messages.data import MISSING_DATA
from wsgilib import JSON

from dscms4.menu.item import get_menu_item


__all__ = ['ROUTES']


def get_chart(type_, ident):
    """Gets a chart by type and ID."""

    try:
        type_ = Chart.types[type_]
    except KeyError:
        raise INVALID_CHART_TYPE

    try:
        return type_.select().join(BaseChart).where(
            (BaseChart.customer == CUSTOMER) & (type_.id == ident)).get()
    except type_.DoesNotExist:
        raise NO_SUCH_CHART


def get_menu_item_chart(ident):
    """Returns the respective MenuItemChart."""

    try:
        return MenuItemChart.select().join(MenuItem).join(Menu).where(
            (Menu.customer == CUSTOMER.id) & (MenuItemChart.id == ident)).get()
    except MenuItemChart.DoesNotExist:
        raise NO_SUCH_MENU_ITEM_CHART


@authenticated
@authorized('dscms4')
def list_(ident):
    """Lists the respective menu's items."""

    return JSON([chart.to_json() for chart in get_menu_item(ident).charts])


@authenticated
@authorized('dscms4')
def add():
    """Adds a new menu item."""

    json = dict(JSON_DATA)

    try:
        menu_item = json.pop('menu_item')
    except KeyError:
        raise MISSING_DATA.update(key='menu_item')

    menu_item = get_menu_item(menu_item)

    try:
        chart = json.pop('chart')
    except KeyError:
        raise MISSING_DATA.update(key='chart')

    try:
        type_ = chart['type']
    except KeyError:
        raise MISSING_DATA.update(key='chart→type')

    try:
        chart_id = chart['id']
    except KeyError:
        raise MISSING_DATA.update(key='chart→id')

    chart = get_chart(type_, chart_id)
    menu_item_chart = MenuItemChart.from_json(json, menu_item, chart.base)
    menu_item_chart.save()
    return MENU_ITEM_CHART_ADDED.update(id=menu_item_chart.id)


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes a menu or menu item."""

    get_menu_item_chart(ident).delete_instance()
    return MENU_ITEM_CHART_DELETED


@authenticated
@authorized('dscms4')
def order():
    """Orders the respective menu items."""

    menu_item_charts = (get_menu_item_chart(ident) for ident in JSON_DATA)

    try:
        first, *other = menu_item_charts
    except ValueError:
        return MENU_ITEM_CHARTS_SORTED  # Empty set of MenuItemsCharts.

    if all(menu_item_chart.menu_item == first.menu_item
           for menu_item_chart in other):
        for index, menu_item_chart in enumerate(chain((first,), other)):
            menu_item_chart.index = index
            menu_item_chart.save()

        return MENU_ITEM_CHARTS_SORTED

    return DIFFERENT_MENU_ITEMS


ROUTES = (
    ('GET', '/menu/item/<ident>/charts', list_, 'list_menu_item_charts'),
    ('POST', '/menu/item/chart', add, 'add_menu_item_chart'),
    ('DELETE', '/menu/item/chart/<int:ident>', delete,
     'delete_menu_item_chart'),
    ('POST', '/menu/item/chart/order', order, 'order_menu_item_charts'))
