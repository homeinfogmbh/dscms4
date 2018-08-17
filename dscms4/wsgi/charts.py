"""DSCMS4 WSGI handlers for charts."""

from flask import request
from werkzeug.local import LocalProxy

from his import CUSTOMER, authenticated, authorized
from his.messages import InvalidData
from peeweeplus import InvalidKeys
from wsgilib import JSON

from dscms4.messages.charts import NoChartTypeSpecified, InvalidChartType, \
    NoChartIdSpecified, NoSuchChart, ChartAdded, ChartDeleted, ChartPatched
from dscms4.messages.common import InvalidId
from dscms4.orm.charts import CHARTS

__all__ = ['get_chart', 'CHART_TYPES', 'CHART_TYPE', 'CHARTS', 'ROUTES']


def get_chart_types():
    """Yields selected chart types."""

    try:
        type_names = request.args['types']
    except KeyError:
        yield from CHARTS.values()
    else:
        for type_name in type_names.split(','):
            try:
                yield CHARTS[type_name]
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
        for chart in typ.by_customer(CUSTOMER.id):
            yield chart


def get_chart(ident):
    """Returns the selected chart."""

    try:
        return CHART_TYPE.by_id(ident, customer=CUSTOMER.id)
    except CHART_TYPE.DoesNotExist:
        raise NoSuchChart()


def get_brief():
    """Returns whether a brief data set is requested."""

    return 'brief' in request.args


@authenticated
@authorized('dscms4')
def list_():
    """Lists IDs of charts of the respective customer."""

    return JSON([chart.to_json(brief=get_brief()) for chart in get_charts()])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective chart of the current customer."""

    return JSON(get_chart(ident).to_json(brief=get_brief()))


@authenticated
@authorized('dscms4')
def add():
    """Adds new charts."""

    try:
        transaction = CHART_TYPE.from_json(CUSTOMER, request.json)
    except InvalidKeys as invalid_keys:
        raise InvalidData(invalid_keys=invalid_keys.invalid_keys)

    transaction.commit()
    return ChartAdded(id=transaction.chart.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches a chart."""

    chart = get_chart(ident)

    try:
        transaction = chart.patch_json(request.json)
    except InvalidKeys as invalid_keys:
        raise InvalidData(invalid_keys=invalid_keys.invalid_keys)

    transaction.commit()
    return ChartPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes the specified chart."""

    get_chart(ident).delete_instance()
    return ChartDeleted()


ROUTES = (
    ('GET', '/charts', list_, 'list_charts'),
    ('GET', '/charts/<int:ident>', get, 'get_charts'),
    ('POST', '/charts', add, 'add_chart'),
    ('PATCH', '/charts/<int:ident>', patch, 'patch_chart'),
    ('DELETE', '/charts/<int:ident>', delete, 'delete_chart'))
