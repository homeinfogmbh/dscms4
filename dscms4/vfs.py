"""Virtual file system."""

from flask import request

from cmslib import Directory
from cmslib import get_base_chart
from cmslib import get_unassigned_base_charts
from cmslib import get_directory
from cmslib import get_root
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage, require_json


__all__ = ["ROUTES"]


@authenticated
@authorized("dscms4")
def list_root() -> JSON:
    """Lists the directories."""

    return JSON(
        {
            "directories": [
                directory.to_json(children=True) for directory in get_root(CUSTOMER.id)
            ],
            "baseCharts": [
                base_chart.id for base_chart in get_unassigned_base_charts(CUSTOMER.id)
            ],
        }
    )


@authenticated
@authorized("dscms4")
def get(ident: int) -> JSON:
    """Lists a specific directory."""

    return JSON(
        get_directory(ident, CUSTOMER.id).to_json(children=True, base_charts=True)
    )


@authenticated
@authorized("dscms4")
@require_json(dict)
def add() -> JSONMessage:
    """Adds a new directory."""

    parent = request.json.pop("parent", None)

    if parent is not None:
        parent = get_directory(parent, CUSTOMER.id)

    directory = Directory.from_json(request.json, CUSTOMER.id, parent)
    directory.save()
    return JSONMessage("Directory added.", id=directory.id, status=201)


@authenticated
@authorized("dscms4")
@require_json(dict)
def patch(ident: int) -> JSONMessage:
    """Patches the respective directory."""

    directory = get_directory(ident, CUSTOMER.id)
    directory.patch_json(request.json)
    directory.save()
    return JSONMessage("Directory patched.", status=200)


@authenticated
@authorized("dscms4")
def delete(ident: int) -> JSONMessage:
    """Deletes the respective directory."""

    get_directory(ident, CUSTOMER.id).delete_instance()
    return JSONMessage("Directory deleted.", status=200)


@authenticated
@authorized("dscms4")
@require_json(dict)
def add_base_chart(ident: int) -> JSONMessage:
    """Adds a base chart to the respective directory."""

    directory = get_directory(ident, CUSTOMER.id)
    directory.add_base_chart(get_base_chart(request.json["baseChart"], CUSTOMER.id))
    return JSONMessage("Base chart added.", status=201)


@authenticated
@authorized("dscms4")
def remove_base_chart(ident: int, base_chart: int) -> JSONMessage:
    """Removes a base chart from the respective directory."""

    directory = get_directory(ident, CUSTOMER.id)
    directory.remove_base_chart(base_chart)
    return JSONMessage("Base charts removed.", status=200)


ROUTES = (
    ("GET", "/vfs", list_root),
    ("GET", "/vfs/<int:ident>", get),
    ("POST", "/vfs", add),
    ("PATCH", "/vfs/<int:ident>", patch),
    ("DELETE", "/vfs/<int:ident>", delete),
    ("POST", "/vfs/<int:ident>/chart", add_base_chart),
    ("DELETE", "/vfs/<int:ident>/chart/<int:base_chart>", remove_base_chart),
)
