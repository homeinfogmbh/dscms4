"""Controllers for chart types."""

from collections import defaultdict

from flask import request

from cmslib.functions.charts import get_chart_acls
from cmslib.orm.chart_acl import ChartACL
from cmslib.orm.charts import CHARTS
from his import authenticated, authorized, root, require_json
from mdb import Customer
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists available chart types."""

    return JSON([acl.to_json() for acl in get_chart_acls()])


@authenticated
@root
def all_() -> JSON:
    """Returns a mapping of all charts types of all customers."""

    chart_types = defaultdict(list)

    for chart_type in ChartACL.select(cascade=True).where(True):
        json = chart_type.to_json(skip={'customer'})
        chart_types[chart_type.customer.id].append(json)

    return JSON(chart_types)


@authenticated
@root
@require_json(dict)
def add() -> JSONMessage:
    """Adds a chart type for the respective customer."""

    customer = request.json.get('customer')
    chart_type = request.json.get('chartType')
    customer = Customer.get(Customer.id == customer)
    _ = CHARTS[chart_type]  # Test whether type is valid.
    record = ChartACL(customer=customer, chart_type=chart_type)
    record.save()
    return JSONMessage('Chart ACL added.', id=record.id, status=201)


@authenticated
@root
def delete(ident: int) -> JSONMessage:
    """Adds a chart type for the respective customer."""

    ChartACL[ident].delete_instance()
    return JSONMessage('Chart ACL deleted.', status=200)


ROUTES = [
    ('GET', '/chart-types', list_),
    ('GET', '/chart-types/all', all_),
    ('POST', '/chart-types', add),
    ('DELETE', '/chart-types/<int:ident>', delete)
]
