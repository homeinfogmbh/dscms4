"""DSCMS4 WSGI handlers for charts."""

from collections import defaultdict

from flask import request

from cmslib import CHART_TYPE
from cmslib import get_base_chart
from cmslib import get_chart
from cmslib import get_charts
from cmslib import get_mode
from his import authenticated, authorized, require_json
from wsgilib import JSON, JSONMessage, get_bool


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists IDs of charts of the respective customer."""

    if get_bool('assoc'):
        charts = defaultdict(dict)

        for chart in get_charts():
            charts[type(chart).__name__][chart.id] = chart.to_json(
                mode=get_mode())

        return JSON(charts)

    return JSON([chart.to_json(mode=get_mode()) for chart in get_charts()])


@authenticated
@authorized('dscms4')
def get_chart_(ident: int) -> JSON:
    """Returns the respective chart of the current customer."""

    return JSON(get_chart(ident).to_json(mode=get_mode()))


@authenticated
@authorized('dscms4')
def get_base_chart_(ident: int) -> JSON:
    """Returns the respective base chart of the current customer."""

    return JSON(get_base_chart(ident).to_json())


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds new charts."""

    transaction = CHART_TYPE.from_json(request.json)
    transaction.commit()
    return JSONMessage(
        'Chart added.', id=transaction.id, base_chart=transaction.base.id,
        status=201)


@authenticated
@authorized('dscms4')
@require_json(dict)
def patch(ident: int) -> JSONMessage:
    """Patches a chart."""

    chart = get_chart(ident)
    transaction = chart.patch_json(request.json)
    transaction.commit()
    return JSONMessage('Chart patched.', status=200)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes the specified chart."""

    get_chart(ident).delete_instance()
    return JSONMessage('Chart deleted.', status=200)


ROUTES = [
    ('GET', '/charts', list_),
    ('GET', '/charts/<int:ident>', get_chart_),
    ('GET', '/base-chart/<int:ident>', get_base_chart_),
    ('POST', '/charts', add),
    ('PATCH', '/charts/<int:ident>', patch),
    ('DELETE', '/charts/<int:ident>', delete)
]
