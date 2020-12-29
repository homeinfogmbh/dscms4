"""DSCMS4 WSGI handlers for menu item charts."""

from cmslib.functions.charts import get_chart
from cmslib.functions.menu import get_menu_item, get_menu_item_chart
from cmslib.messages.charts import INVALID_CHART_TYPE
from cmslib.messages.menu import MENU_ITEM_CHART_ADDED
from cmslib.messages.menu import MENU_ITEM_CHART_DELETED
from cmslib.messages.menu import MENU_ITEM_CHART_PATCHED
from cmslib.orm.charts import CHARTS
from cmslib.orm.menu import MenuItemChart
from his import JSON_DATA, authenticated, authorized
from his.messages.data import MISSING_DATA
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


EXCLUDED_FIELDS = {'menu_item', 'base_chart'}


@authenticated
@authorized('dscms4')
def list_(ident: int) -> JSON:
    """Lists the respective menu's items."""

    return JSON([chart.to_json() for chart in get_menu_item(ident).charts])


@authenticated
@authorized('dscms4')
def add() -> JSONMessage:
    """Adds a new menu item."""

    json = dict(JSON_DATA)

    try:
        menu_item = json.pop('menu_item')
    except KeyError:
        return MISSING_DATA.update(key='menu_item')

    menu_item = get_menu_item(menu_item)

    try:
        chart = json.pop('chart')
    except KeyError:
        return MISSING_DATA.update(key='chart')

    try:
        typename = chart['type']
    except KeyError:
        return MISSING_DATA.update(key='chart→type')

    try:
        cls = CHARTS[typename]
    except KeyError:
        return INVALID_CHART_TYPE

    try:
        chart_id = chart['id']
    except KeyError:
        return MISSING_DATA.update(key='chart→id')

    chart = get_chart(chart_id, cls=cls)
    menu_item_chart = MenuItemChart.from_json(json, menu_item, chart.base)
    menu_item_chart.save()
    return MENU_ITEM_CHART_ADDED.update(id=menu_item_chart.id)


@authenticated
@authorized('dscms4')
def patch(ident: int) -> JSONMessage:
    """Orders the respective menu items."""

    menu_item_chart = get_menu_item_chart(ident)
    json = dict(JSON_DATA)
    menu_item_chart.patch_json(json, skip=EXCLUDED_FIELDS)
    menu_item_chart.save()
    return MENU_ITEM_CHART_PATCHED


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes a menu or menu item."""

    get_menu_item_chart(ident).delete_instance()
    return MENU_ITEM_CHART_DELETED


ROUTES = (
    ('GET', '/menu/item/<ident>/charts', list_),
    ('POST', '/menu/item/chart', add),
    ('PATCH', '/menu/item/chart/<int:ident>', patch),
    ('DELETE', '/menu/item/chart/<int:ident>', delete)
)
