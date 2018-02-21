"""Controllers for chart types."""

from his import CUSTOMER, authenticated, authorized, root
from wsgilib import JSON

from homeinfo.crm import Customer

from dscms4.orm.chart_types import ChartType
from dscms4.orm.charts import CHARTS
from dscms4.messages.customer import NoSuchCustomer
from dscms4.messages.chart_types import InvalidChartType, ChartTypeAdded

__all__ = ['ROUTES']


def _get_customer(cid):
    """Returns the respective customer."""

    try:
        return Customer.get(Customer.id == cid)
    except Customer.DoesNotExist:
        raise NoSuchCustomer()


def _validate_type(chart_type):
    """Checks whether the respective chart type actually exists."""

    try:
        return CHARTS[chart_type]
    except KeyError:
        raise InvalidChartType()


def _get_chart_types():
    """Yields chart types this customer may use."""

    return ChartType.select().where(ChartType.customer == CUSTOMER.id)


@authenticated
@authorized('dscms4')
def list_():
    """Lists available chart types."""

    return JSON([chart_type.to_dict() for chart_type in _get_chart_types()])


@authenticated
@root
def add(cid, chart_type):
    """Adds a chart type for the respective customer."""

    chart_type = ChartType.add(_get_customer(cid), _validate_type(chart_type))
    chart_type.save()
    return ChartTypeAdded()


ROUTES = (
    ('GET', '/chart-types', list_, 'list_chart_types'),
    ('POST', '/chart-types/<int:cid>/<chart_type>', add, 'add_chart_type'))
