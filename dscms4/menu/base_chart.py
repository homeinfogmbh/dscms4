"""DSCMS4 WSGI handlers for menu item charts."""

from flask import request

from cmslib import MenuItemChart
from cmslib import get_base_chart
from cmslib import get_menu_item
from cmslib import get_menu_item_chart
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage, require_json


__all__ = ["ROUTES"]


EXCLUDED_FIELDS = {"menu_item", "base_chart"}


@authenticated
@authorized("dscms4")
def list_(ident: int) -> JSON:
    """Lists the respective menu's items."""

    return JSON([chart.to_json() for chart in get_menu_item(ident, CUSTOMER.id).charts])


@authenticated
@authorized("dscms4")
@require_json(dict)
def add() -> JSONMessage:
    """Adds a new menu item."""

    menu_item = get_menu_item(request.json.pop("menuItem"), CUSTOMER.id)
    base_chart = get_base_chart(request.json.pop("baseChart"), CUSTOMER.id)
    record = MenuItemChart.from_json(request.json, menu_item, base_chart)
    record.save()
    return JSONMessage("Menu item chart added.", id=record.id, status=201)


@authenticated
@authorized("dscms4")
@require_json(dict)
def patch(ident: int) -> JSONMessage:
    """Orders the respective menu items."""

    record = get_menu_item_chart(ident, CUSTOMER.id)
    record.patch_json(request.json, skip=EXCLUDED_FIELDS)
    record.save()
    return JSONMessage("Menu item chart patched.", status=200)


@authenticated
@authorized("dscms4")
def delete(ident: int) -> JSONMessage:
    """Deletes a menu or menu item."""

    get_menu_item_chart(ident, CUSTOMER.id).delete_instance()
    return JSONMessage("Menu item chart deleted.", status=200)


ROUTES = [
    ("GET", "/menu/item/<ident>/base_charts", list_),
    ("POST", "/menu/item/base_chart", add),
    ("PATCH", "/menu/item/base_chart/<int:ident>", patch),
    ("DELETE", "/menu/item/base_chart/<int:ident>", delete),
]
