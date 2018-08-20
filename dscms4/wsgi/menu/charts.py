"""DSCMS4 WSGI handlers for menu item charts."""

from itertools import chain

from flask import request

from his import authenticated, authorized
from his.messages import MissingData
from wsgilib import JSON

from dscms4.messages.charts import InvalidChartType, NoSuchChart
from dscms4.messages.menu import NoSuchMenuItemChart, MenuItemChartAdded, \
    MenuItemChartDeleted, DifferentMenuItemsError, MenuItemChartsSorted
from dscms4.orm.charts import CHARTS
from dscms4.orm.menu import MenuItemChart
from dscms4.wsgi.menu.item import get_menu_item


__all__ = ['ROUTES']


def get_chart(type_, ident):
    """Gets a chart by type and ID."""

    try:
        type_ = CHARTS[type_]
    except KeyError:
        raise InvalidChartType()

    try:
        return type_.get(type_.id == ident)
    except type_.DoesNotExist:
        raise NoSuchChart()


def get_menu_item_chart(ident):
    """Returns the respective MenuItemChart."""

    try:
        return MenuItemChart.cget(MenuItemChart.id == ident)
    except MenuItemChart.DoesNotExist:
        raise NoSuchMenuItemChart()


@authenticated
@authorized('dscms4')
def list_(ident):
    """Lists the respective menu's items."""

    return JSON([chart.to_dict() for chart in get_menu_item(ident).charts])


@authenticated
@authorized('dscms4')
def add():
    """Adds a new menu item."""

    try:
        menu_item = request.json['menu_item']
    except KeyError:
        raise MissingData(key='menu_item')

    menu_item = get_menu_item(menu_item)

    try:
        chart = request.json['chart']
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
    menu_item_chart = MenuItemChart.add(menu_item, chart.base)
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

    menu_item_charts = (get_menu_item_chart(ident) for ident in request.json)

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
