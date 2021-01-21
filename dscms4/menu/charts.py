"""DSCMS4 WSGI handlers for menu item charts."""

from cmslib.functions.charts import get_chart
from cmslib.functions.menu import get_menu_item, get_menu_item_chart
from cmslib.orm.charts import CHARTS
from cmslib.orm.menu import MenuItemChart
from his import authenticated, authorized, require_json
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
@require_json(dict)
def add() -> JSONMessage:
    """Adds a new menu item."""

    menu_item = get_menu_item(request.json.pop('menuItem'))
    base_chart = get_base_chart(request.json.pop('baseChart'))
    record = MenuItemChart.from_json(request.json, menu_item, base_chart)
    record.save()
    return JSONMessage('Menu item chart added.', id=record.id, status=201)


@authenticated
@authorized('dscms4')
def patch(ident: int) -> JSONMessage:
    """Orders the respective menu items."""

    menu_item_chart = get_menu_item_chart(ident)
    menu_item_chart.patch_json(request.json, skip=EXCLUDED_FIELDS)
    menu_item_chart.save()
    return JSONMessage('Menu item chart patched.', status=200)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes a menu or menu item."""

    get_menu_item_chart(ident).delete_instance()
    return JSONMessage('Menu item chart deleted.', status=200)


ROUTES = (
    ('GET', '/menu/item/<ident>/charts', list_),
    ('POST', '/menu/item/chart', add),
    ('PATCH', '/menu/item/chart/<int:ident>', patch),
    ('DELETE', '/menu/item/chart/<int:ident>', delete)
)
