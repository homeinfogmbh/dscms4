"""DSCMS4 WSGI handlers for charts."""

from flask import request
from his import CUSTOMER, DATA, authenticated, authorized
from werkzeug.local import LocalProxy
from wsgilib import JSON

from dscms4.messages.charts import ChartDataIncomplete, ChartDataInvalid, \
    NoChartTypeSpecified, InvalidChartType, NoChartIdSpecified, \
    NoSuchChart, ChartAdded, ChartDeleted, ChartPatched
from dscms4.messages.common import InvalidId
from dscms4.orm.charts import CHARTS, Chart

__all__ = ['get_chart', 'CHART_TYPES', 'CHART_TYPE', 'CHARTS', 'ROUTES']


def get_chart_types():
    """Yields selected chart types."""

    try:
        chart_types = request.args['types']
    except KeyError:
        yield from CHARTS.values()
    else:
        for chart_type in chart_types.split(','):
            try:
                yield CHARTS[chart_type]
            except KeyError:
                raise InvalidChartType()


CHART_TYPES = LocalProxy(get_chart_types)


def get_chart_type():
    """Returns the selected chart type."""

    try:
        chart_type = request.args['type']
    except KeyError:
        raise NoChartTypeSpecified()

    try:
        return CHARTS[chart_type]
    except KeyError:
        raise InvalidChartType()


CHART_TYPE = LocalProxy(get_chart_type)


def get_chart_id(ident):
    """Returns the specified chart ID."""

    try:
        return int(ident)
    except TypeError:
        raise NoChartIdSpecified()
    except ValueError:
        raise InvalidId()


def get_charts():
    """Lists the available charts."""

    for typ in CHART_TYPES:
        print('Type:', typ, 'customer ID:', CUSTOMER.id, flush=True)
        for chart in typ.select().join(BaseChart).where(
                typ.customer == CUSTOMER.id):
            print('Chart:', chart, flush=True)
            yield chart


def get_chart(ident):
    """Returns the selected chart."""

    try:
        return CHART_TYPE.get(
            (CHART_TYPE.id == ident) & (CHART_TYPE.customer == CUSTOMER.id))
    except CHART_TYPE.DoesNotExist:
        raise NoSuchChart()


@authenticated
@authorized('dscms4')
def lst():
    """Lists IDs of charts of the respective customer."""

    return JSON([chart.to_dict() for chart in get_charts()])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective chart of the current customer."""

    return JSON(get_chart(ident))


@authenticated
@authorized('dscms4')
def add():
    """Adds new charts."""

    chart_dict = DATA.json
    ident = None

    for record in CHART_TYPE.from_dict(CUSTOMER, chart_dict):
        record.save()

        if isinstance(record, Chart):
            ident = record.id

    return ChartAdded(id=ident)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches a chart."""

    chart = get_chart(ident)
    chart.patch(DATA.json)

    if chart.trashed:
        chart.delete_instance()

    return ChartPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes the specified chart."""

    get_chart(ident).remove()
    return ChartDeleted()


ROUTES = (
    ('GET', '/charts', lst, 'list_charts'),
    ('GET', '/charts/<int:ident>', get, 'get_charts'),
    ('POST', '/charts', add, 'add_chart'),
    ('PATCH', '/charts/<int:ident>', patch, 'patch_chart'),
    ('DELETE', '/charts/<int:ident>', delete, 'delete_chart'))
