"""Controllers for chart types."""

from his import CUSTOMER, authenticated, authorized, root
from his.messages import NoSuchCustomer
from mdb import Customer
from wsgilib import JSON

from dscms4.orm.chart_types import ChartType
from dscms4.orm.charts import CHARTS
from dscms4.messages.charts import InvalidChartType, ChartTypeAdded


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_():
    """Lists available chart types."""

    chart_types = ChartType.select().where(ChartType.customer == CUSTOMER.id)
    return JSON([chart_type.to_json() for chart_type in chart_types])


@authenticated
@root
def add(cid, chart_type):
    """Adds a chart type for the respective customer."""

    try:
        customer = Customer.get(Customer.id == cid)
    except Customer.DoesNotExist:
        return NoSuchCustomer()

    try:
        chart_type = CHARTS[chart_type]
    except KeyError:
        return InvalidChartType()

    chart_type = ChartType.add(chart_type)
    chart_type.save()
    return ChartTypeAdded()


ROUTES = (
    ('GET', '/chart-types', list_, 'list_chart_types'),
    ('POST', '/chart-types/<int:cid>/<chart_type>', add, 'add_chart_type'))
