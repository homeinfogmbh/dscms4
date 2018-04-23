"""DSCMS4 WSGI handlers for menu item charts."""

from his import CUSTOMER, DATA, authenticated, authorized
from his.messages import MissingData
from wsgilib import JSON

from dscms4.messages.charts import InvalidChartType, NoSuchChart
from dscms4.messages.menu import NoSuchMenuItemChart, MenuItemChartAdded, \
    MenuItemChartDeleted, DifferentMenuItemsError, MenuItemChartsSorted
from dscms4.orm.charts import CHARTS, BaseChart
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
        return type_.join(BaseChart).select().where(
            (BaseChart.customer == CUSTOMER.id) & (type_.id == ident))
    except type_.DoesNotExist:
        raise NoSuchChart()


def get_menu_item_chart(ident):
    """Returns the respective menu item chart."""

    try:
        return MenuItemChart.get(
            (MenuItemChart.customer == CUSTOMER.id)
            & (MenuItemChart.id == ident))
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

    menu_item_chart = DATA.json

    try:
        menu_item = menu_item_chart.pop('menu_item')
    except KeyError:
        raise MissingData(key='menu_item')

    menu_item = get_menu_item(menu_item)

    try:
        chart = menu_item_chart.pop('chart')
    except KeyError:
        raise MissingData(key='chart')

    try:
        type_ = chart.pop('type')
    except KeyError:
        raise MissingData(key='chart→type')

    try:
        chart_id = chart.pop('id')
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

    mi_charts = tuple(get_menu_item_chart(ident) for ident in DATA.json)

    try:
        sentinel = mi_charts[0].menu_item
    except IndexError:
        return MenuItemChartsSorted()    # Empty list.

    if all(mi_chart.menu_item == sentinel for mi_chart in mi_charts[1:]):
        for index, mi_chart in enumerate(mi_charts):
            mi_chart.index = index
            mi_chart.save()

        return MenuItemChartsSorted()

    return DifferentMenuItemsError()


ROUTES = (
    ('GET', '/menu/item/<ident>/charts', list_, 'list_menu_item_charts'),
    ('POST', '/menu/item/chart', add, 'add_menu_item_chart'),
    ('DELETE', '/menu/item/chart/<int:ident>', delete,
     'delete_menu_item_chart'),
    ('POST', '/menu/item/chart/order', order, 'order_menu_item_charts'))
