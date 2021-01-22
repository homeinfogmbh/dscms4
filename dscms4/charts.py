"""DSCMS4 WSGI handlers for charts."""

from collections import defaultdict

from flask import request

from cmslib.functions.charts import CHART_TYPE
from cmslib.functions.charts import get_chart
from cmslib.functions.charts import get_charts
from cmslib.functions.charts import get_mode
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

    charts = [chart.to_json(mode=get_mode()) for chart in get_charts()]
    print('CHARTS:', len(charts), flush=True)
    print('CHARTS:', [chart.keys() for chart in charts], flush=True)
    return JSON(charts)


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the respective chart of the current customer."""

    return JSON(get_chart(ident).to_json(mode=get_mode()))


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds new charts."""

    transaction = CHART_TYPE.from_json(request.json)
    transaction.commit()
    return JSONMessage('Chart added.', id=transaction.id, status=201)


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
    ('GET', '/charts/<int:ident>', get),
    ('POST', '/charts', add),
    ('PATCH', '/charts/<int:ident>', patch),
    ('DELETE', '/charts/<int:ident>', delete)
]
