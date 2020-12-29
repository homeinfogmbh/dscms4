"""Controllers for chart types."""

from collections import defaultdict

from cmslib.orm.chart_acl import ChartACL
from cmslib.orm.charts import CHARTS
from cmslib.messages.charts import CHART_TYPE_ADDED
from cmslib.messages.charts import CHART_TYPE_DELETED
from cmslib.messages.charts import INVALID_CHART_TYPE
from cmslib.messages.charts import NO_SUCH_CHART_TYPE
from his import CUSTOMER, JSON_DATA, authenticated, authorized, root
from his.messages.customer import NO_SUCH_CUSTOMER
from mdb import Customer
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists available chart types."""

    chart_types = ChartACL.select().where(ChartACL.customer == CUSTOMER.id)
    return JSON([chart_type.to_json() for chart_type in chart_types])


@authenticated
@root
def all_() -> JSON:
    """Returns a mapping of all charts types of all customers."""

    chart_types = defaultdict(list)

    for chart_type in ChartACL:
        json = chart_type.to_json(skip={'customer'})
        chart_types[chart_type.customer.id].append(json)

    return JSON(chart_types)


@authenticated
@root
def add() -> JSONMessage:
    """Adds a chart type for the respective customer."""

    customer = JSON_DATA.get('customer')
    chart_type = JSON_DATA.get('chartType')

    try:
        customer = Customer.get(Customer.id == customer)
    except Customer.DoesNotExist:
        return NO_SUCH_CUSTOMER

    try:
        CHARTS[chart_type]  # Test whether type is valid.
    except KeyError:
        return INVALID_CHART_TYPE

    chart_type = ChartACL(customer=customer, chart_type=chart_type)
    chart_type.save()
    return CHART_TYPE_ADDED.update(id=chart_type.id)


@authenticated
@root
def delete(ident: int) -> JSONMessage:
    """Adds a chart type for the respective customer."""

    try:
        chart_type = ChartACL[ident]
    except ChartACL.DoesNotExist:
        return NO_SUCH_CHART_TYPE

    chart_type.delete_instance()
    return CHART_TYPE_DELETED


ROUTES = (
    ('GET', '/chart-types', list_),
    ('GET', '/chart-types/all', all_),
    ('POST', '/chart-types', add),
    ('DELETE', '/chart-types/<int:ident>', delete)
)
