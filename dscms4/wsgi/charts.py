"""DSCMS4 WSGI handlers for charts."""

from peewee import DoesNotExist

from wsgilib import JSON

from dscms4.wsgi.messages.charts import ChartDataIncomplete, ChartDataInvalid,\
    NoChartTypeSpecified, InvalidChartType, NoChartIdSpecified, \
    NoSuchChart, ChartAdded, ChartDeleted, ChartPatched, InvalidId
from dscms4.orm.charts import CHARTS
from dscms4.orm.exceptions import InvalidData, MissingData

__all__ = ['ROUTES']


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
        for _, chart_type in CHARTS.items():
            yield chart_type
    else:
        for chart_type in _parse_chart_types(chart_types):
            try:
                yield CHARTS[chart_type]
            except KeyError:
                raise InvalidChartType()


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


def _get_chart_id(ident):
    """Returns the specified chart ID."""

    try:
        return int(self.resource)
    except TypeError:
        raise NoChartIdSpecified()
    except ValueError:
        raise InvalidId()


def _get_charts():
    """Lists the available charts."""

    for typ in _get_chart_types():
        for chart in typ.select().where(typ.customer == CUSTOMER.id):
            yield chart


def _get_chart(ident):
    """Returns the selected chart."""

    typ = _get_chart_type()

    try:
        return typ.get((typ.id == ident) & (typ.customer == CUSTOMER.id))
    except DoesNotExist:
        raise NoSuchChart()


def lst():
    """Lists IDs of charts of the respective customer."""

    return JSON([chart.to_dict() for chart in _get_charts()])


def get(ident):
    """Returns the respective chart of the current customer."""

    return JSON(_get_chart(ident))


def add():
    """Adds new charts."""

    chart_dict = DATA.json
    chart_type = _get_chart_type()

    try:
        chart = chart_type.from_dict(chart_dict)
    except MissingData as missing_data:
        raise ChartDataIncomplete(missing_data.missing)
    except InvalidData as invalid_data:
        raise ChartDataInvalid(invalid_data.invalid)

    return ChartAdded(id=chart.id)


def delete(ident):
    """Deletes the specified chart."""

    typ = _get_chart_type()

    try:
        chart = typ.get(typ.id == ident)
    except DoesNotExist:
        raise NoSuchChart()

    chart.remove()
    return ChartDeleted()


def patch(ident):
    """Patches a chart."""

    chart = _get_chart(ident)
    chart.patch(DATA.json)

    if chart.trashed:
        _delete_from_contents(chart)

    return ChartPatched()


ROUTES = (
    ('/charts', 'GET', lst),
    ('/charts/<int:ident>', 'GET', get),
    ('/charts', 'POST', add),
    ('/charts/<int:ident>', 'DELETE', delete),
    ('/charts/<int:ident>', 'PATCH', patch))
