"""DSCMS4 WSGI handlers for charts."""

from collections import defaultdict

from flask import request
from werkzeug.local import LocalProxy

from cmslib.messages.charts import NO_CHART_TYPE_SPECIFIED
from cmslib.messages.charts import INVALID_CHART_TYPE
from cmslib.messages.charts import NO_SUCH_CHART
from cmslib.messages.charts import CHART_ADDED
from cmslib.messages.charts import CHART_DELETED
from cmslib.messages.charts import CHART_PATCHED
from cmslib.orm.charts import ChartMode, BaseChart, Chart
from his import CUSTOMER, JSON_DATA, authenticated, authorized
from his.messages.data import INVALID_DATA, NOT_AN_INTEGER
from peeweeplus import InvalidKeys
from wsgilib import JSON


__all__ = ['get_chart', 'CHART_TYPES', 'CHART_TYPE', 'ROUTES']


def get_chart_types():
    """Yields selected chart types."""

    try:
        type_names = request.args['types']
    except KeyError:
        yield from Chart.types.values()
        return

    for type_name in type_names.split(','):
        try:
            yield Chart.types[type_name]
        except KeyError:
            raise INVALID_CHART_TYPE


CHART_TYPES = LocalProxy(get_chart_types)


def get_chart_type():
    """Returns the selected chart type."""

    try:
        chart_type = request.args['type']
    except KeyError:
        raise NO_CHART_TYPE_SPECIFIED

    try:
        return Chart.types[chart_type]
    except KeyError:
        raise INVALID_CHART_TYPE


CHART_TYPE = LocalProxy(get_chart_type)


def get_trashed():
    """Returns a selection for the trashed status."""

    trashed = request.args.get('trashed')

    if trashed is None:
        return True     # Don't care.

    try:
        trashed = int(trashed)
    except ValueError:
        raise NOT_AN_INTEGER.update(key='trashed', value=trashed)

    if trashed:
        return BaseChart.trashed == 1

    return BaseChart.trashed == 0


def get_charts():
    """Lists the available charts."""

    for typ in CHART_TYPES:
        for record in typ.select().join(BaseChart).where(
                (BaseChart.customer == CUSTOMER.id) & get_trashed()):
            yield record


def get_chart(ident):
    """Returns the selected chart."""

    try:
        return CHART_TYPE.select().join(BaseChart).where(
            (BaseChart.customer == CUSTOMER.id)
            & (CHART_TYPE.id == ident)).get()
    except CHART_TYPE.DoesNotExist:
        raise NO_SUCH_CHART


def get_mode():
    """Determines the extend of the dataset."""

    try:
        mode = request.args['mode']
    except KeyError:
        return ChartMode.FULL

    try:
        return ChartMode(mode)
    except ValueError:
        raise INVALID_DATA.update(key='mode', value=mode)


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
