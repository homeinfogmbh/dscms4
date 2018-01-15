"""DSCMS4 WSGI handlers for charts."""

from peewee import DoesNotExist

from flask import request
from his import CUSTOMER, DATA, authenticated, authorized
from his.messages import InvalidData, MissingData
from werkzeug.local import LocalProxy
from wsgilib import JSON

from dscms4.messages.charts import ChartDataIncomplete, ChartDataInvalid, \
    NoChartTypeSpecified, InvalidChartType, NoChartIdSpecified, \
    NoSuchChart, ChartAdded, ChartDeleted, ChartPatched
from dscms4.messages.common import InvalidId
from dscms4.orm.charts import CHARTS

__all__ = ['CHART_TYPES', 'CHART_TYPE', 'CHARTS', 'ROUTES']


def _parse_chart_types(string, sep=','):
    """Parses the chart type names from the respective string."""

    for item in string.split(sep):
        item = item.strip()

        if item:
            yield item


def _get_chart_types():
    """Yields selected chart types."""

    try:
        chart_types = request.args['types']
    except KeyError:
        yield from CHARTS.values()
    else:
        for chart_type in _parse_chart_types(chart_types):
            try:
                yield CHARTS[chart_type]
            except KeyError:
                raise InvalidChartType()


CHART_TYPES = LocalProxy(_get_chart_types)


def _get_chart_type():
    """Returns the selected chart type."""

    try:
        chart_type = request.args['type']
    except KeyError:
        raise NoChartTypeSpecified()

    try:
        return CHARTS[chart_type]
    except KeyError:
        raise InvalidChartType()


CHART_TYPE = LocalProxy(_get_chart_type)


def _get_chart_id(ident):
    """Returns the specified chart ID."""

    try:
        return int(ident)
    except TypeError:
        raise NoChartIdSpecified()
    except ValueError:
        raise InvalidId()


def _get_charts():
    """Lists the available charts."""

    for typ in CHART_TYPES:
        for chart in typ.select().where(typ.customer == CUSTOMER.id):
            yield chart


CHARTS = LocalProxy(_get_charts)


def _get_chart(ident):
    """Returns the selected chart."""

    try:
        return CHART_TYPE.get(
            (CHART_TYPE.id == ident) & (CHART_TYPE.customer == CUSTOMER.id))
    except DoesNotExist:
        raise NoSuchChart()


@authenticated
@authorized('dscms4')
def lst():
    """Lists IDs of charts of the respective customer."""

    return JSON([chart.to_dict() for chart in CHARTS])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective chart of the current customer."""

    return JSON(_get_chart(ident))


@authenticated
@authorized('dscms4')
def add():
    """Adds new charts."""

    chart_dict = DATA.json

    try:
        chart = CHART_TYPE.from_dict(chart_dict)
    except MissingData as missing_data:
        raise ChartDataIncomplete(missing_data.missing)
    except InvalidData as invalid_data:
        raise ChartDataInvalid(invalid_data.invalid)

    return ChartAdded(id=chart.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches a chart."""

    chart = _get_chart(ident)
    chart.patch(DATA.json)

    if chart.trashed:
        chart.delete_instance()

    return ChartPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes the specified chart."""

    try:
        chart = CHART_TYPE.get(CHART_TYPE.id == ident)
    except DoesNotExist:
        raise NoSuchChart()

    chart.remove()
    return ChartDeleted()


ROUTES = (
    ('GET', '/charts', lst, 'list_charts'),
    ('GET', '/charts/<int:ident>', get, 'get_charts'),
    ('POST', '/charts', add, 'add_chart'),
    ('PATCH', '/charts/<int:ident>', patch, 'patch_chart'),
    ('DELETE', '/charts/<int:ident>', delete, 'delete_chart'))
