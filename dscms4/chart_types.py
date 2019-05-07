"""Controllers for chart types."""

from cmslib.orm.chart_types import ChartType
from cmslib.orm.charts import Chart
from cmslib.messages.charts import INVALID_CHART_TYPE, CHART_TYPE_ADDED
from his import CUSTOMER, JSON_DATA, authenticated, authorized, root
from his.messages.customer import NO_SUCH_CUSTOMER
from mdb import Customer
from wsgilib import JSON


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_():
    """Lists available chart types."""

    chart_types = ChartType.select().where(ChartType.customer == CUSTOMER.id)
    return JSON([chart_type.to_json() for chart_type in chart_types])


@authenticated
@root
def add():
    """Adds a chart type for the respective customer."""

    cid = JSON_DATA.get('cid')
    chart_type = JSON_DATA.get('chartType')

    try:
        customer = Customer.get(Customer.id == cid)
    except Customer.DoesNotExist:
        return NO_SUCH_CUSTOMER

    try:
        Chart.types[chart_type]  # Test whether type is valid.
    except KeyError:
        return INVALID_CHART_TYPE

    chart_type = ChartType(customer=customer, chart_type=chart_type)
    chart_type.save()
    return CHART_TYPE_ADDED


ROUTES = (
    ('GET', '/chart-types', list_),
    ('POST', '/chart-types', add)
)
