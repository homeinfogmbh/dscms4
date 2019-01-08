"""DSCMS4 WSGI handlers for menu item charts."""

from itertools import chain

from his import CUSTOMER, JSON_DATA, authenticated, authorized
from his.messages import MissingData
from wsgilib import JSON

from cmslib.messages.charts import InvalidChartType, NoSuchChart
from cmslib.messages.menu import DifferentMenuItemsError
from cmslib.messages.menu import MenuItemChartAdded
from cmslib.messages.menu import MenuItemChartDeleted
from cmslib.messages.menu import MenuItemChartsSorted
from cmslib.messages.menu import NoSuchMenuItemChart
from cmslib.orm.charts import BaseChart, Chart
from cmslib.orm.menu import Menu, MenuItem, MenuItemChart

from dscms4.wsgi.menu.item import get_menu_item


__all__ = ['ROUTES']


def get_chart(type_, ident):
    """Gets a chart by type and ID."""

    try:
        type_ = Chart.types[type_]
    except KeyError:
        raise InvalidChartType()

    try:
        return type_.select().join(BaseChart).where(
            (BaseChart.customer == CUSTOMER) & (type_.id == ident)).get()
    except type_.DoesNotExist:
        raise NoSuchChart()


def get_menu_item_chart(ident):
    """Returns the respective MenuItemChart."""

    try:
        return MenuItemChart.select().join(MenuItem).join(Menu).where(
            (Menu.customer == CUSTOMER.id) & (MenuItemChart.id == ident)).get()
    except MenuItemChart.DoesNotExist:
        raise NoSuchMenuItemChart()


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
        raise MissingData(key='menu_item')

    menu_item = get_menu_item(menu_item)

    try:
        chart = json.pop('chart')
    except KeyError:
        raise MissingData(key='chart')

    try:
        type_ = chart['type']
    except KeyError:
        raise MissingData(key='chart→type')

    try:
        chart_id = chart['id']
    except KeyError:
        raise MissingData(key='chart→id')

    chart = get_chart(type_, chart_id)
    menu_item_chart = MenuItemChart.from_json(json, menu_item, chart.base)
    menu_item_chart.save()
    return MenuItemChartAdded(id=menu_item_chart.id)


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes a menu or menu item."""

    get_menu_item_chart(ident).delete_instance()
    return MenuItemChartDeleted()


@authenticated
@authorized('dscms4')
def order():
    """Orders the respective menu items."""

    menu_item_charts = (get_menu_item_chart(ident) for ident in JSON_DATA)

    try:
        first, *other = menu_item_charts
    except ValueError:
        return MenuItemChartsSorted()   # Empty set of MenuItemsCharts.

    if all(menu_item_chart.menu_item == first.menu_item
           for menu_item_chart in other):
        for index, menu_item_chart in enumerate(chain((first,), other)):
            menu_item_chart.index = index
            menu_item_chart.save()

        return MenuItemChartsSorted()

    return DifferentMenuItemsError()


ROUTES = (
    ('GET', '/menu/item/<ident>/charts', list_, 'list_menu_item_charts'),
    ('POST', '/menu/item/chart', add, 'add_menu_item_chart'),
    ('DELETE', '/menu/item/chart/<int:ident>', delete,
     'delete_menu_item_chart'),
    ('POST', '/menu/item/chart/order', order, 'order_menu_item_charts'))
