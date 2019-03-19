"""DSCMS4 WSGI handlers for charts."""

from collections import defaultdict

from flask import request

from cmslib.functions.charts import CHART_TYPE
from cmslib.functions.charts import get_chart
from cmslib.functions.charts import get_charts
from cmslib.functions.charts import get_mode
from cmslib.messages.charts import CHART_ADDED
from cmslib.messages.charts import CHART_DELETED
from cmslib.messages.charts import CHART_PATCHED
from cmslib.orm.charts import ChartMode
from his import JSON_DATA, authenticated, authorized
from his.messages.data import INVALID_DATA
from peeweeplus import InvalidKeys
from wsgilib import JSON


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_():
    """Lists IDs of charts of the respective customer."""

    if 'assoc' in request.args:
        charts = defaultdict(dict)

        for chart in get_charts():
            charts[type(chart).__name__][chart.id] = chart.to_json(
                mode=ChartMode.ANON)

        return JSON(charts)

    return JSON([chart.to_json(mode=get_mode()) for chart in get_charts()])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective chart of the current customer."""

    return JSON(get_chart(ident).to_json(mode=get_mode()))


@authenticated
@authorized('dscms4')
def add():
    """Adds new charts."""

    try:
        transaction = CHART_TYPE.from_json(JSON_DATA)
    except InvalidKeys as invalid_keys:
        return INVALID_DATA.update(invalid_keys=invalid_keys.invalid_keys)

    transaction.commit()
    return CHART_ADDED.update(id=transaction.chart.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches a chart."""

    chart = get_chart(ident)

    try:
        transaction = chart.patch_json(JSON_DATA)
    except InvalidKeys as invalid_keys:
        return INVALID_DATA.update(invalid_keys=invalid_keys.invalid_keys)

    transaction.commit()
    return CHART_PATCHED


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes the specified chart."""

    get_chart(ident).delete_instance()
    return CHART_DELETED


ROUTES = (
    ('GET', '/charts', list_, 'list_charts'),
    ('GET', '/charts/<int:ident>', get, 'get_charts'),
    ('POST', '/charts', add, 'add_chart'),
    ('PATCH', '/charts/<int:ident>', patch, 'patch_chart'),
    ('DELETE', '/charts/<int:ident>', delete, 'delete_chart'))
