"""Management of charts in deployments."""

from typing import Iterable

from cmslib.functions.charts import get_chart
from cmslib.functions.deployment import get_deployment
from cmslib.orm.charts import BaseChart
from cmslib.orm.content.deployment import DeploymentBaseChart
from his import CUSTOMER, JSON_DATA, authenticated, authorized
from hwdb import Deployment
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


def list_dbc(deployment: int) -> Iterable[DeploymentBaseChart]:
    """Yields the deployment base charts of the
    current customer for the respective termianl.
    """

    return DeploymentBaseChart.select(cascade=True).where(
        (Deployment.id == deployment)
        & (Deployment.customer == CUSTOMER.id)
        & (BaseChart.trashed == 0))


def get_dbc(deployment: int, ident: int) -> DeploymentBaseChart:
    """Returns the respective deployment base chart."""

    return DeploymentBaseChart.select(cascade=True).where(
        (DeploymentBaseChart.id == ident)
        & (Deployment.id == deployment)
        & (Deployment.customer == CUSTOMER.id)).get()


@authenticated
@authorized('dscms4')
def get(deployment: int) -> JSON:
    """Returns a list of IDs of the charts in the respective deployment."""

    return JSON([dbc.to_json() for dbc in list_dbc(deployment)])


@authenticated
@authorized('dscms4')
def add(deployment: int, chart: int) -> JSONMessage:
    """Adds the chart to the respective deployment."""

    deployment = get_deployment(deployment)
    base_chart = get_chart(chart).base
    dbc = DeploymentBaseChart.from_json(JSON_DATA, deployment, base_chart)
    dbc.save()
    return JSONMessage('Deployment base chart added.', id=dbc.id, status=201)


@authenticated
@authorized('dscms4')
def patch(deployment: int, chart: int) -> JSONMessage:
    """Adds the chart to the respective deployment."""

    dbc = get_dbc(deployment, chart)
    dbc.patch_json(JSON_DATA)
    dbc.save()
    return JSONMessage('Deployment base chart patched.', status=200)


@authenticated
@authorized('dscms4')
def delete(deployment: int, chart: int) -> JSONMessage:
    """Deletes the chart from the respective deployment."""

    dbc = get_dbc(deployment, chart)
    dbc.delete_instance()
    return JSONMessage('Deployment base chart deleted.', status=200)


ROUTES = (
    ('GET', '/content/deployment/<int:deployment>/chart', get),
    ('POST', '/content/deployment/<int:deployment>/chart/<int:chart>', add),
    ('PATCH', '/content/deployment/<int:deployment>/chart/<int:chart>', patch),
    ('DELETE', '/content/deployment/<int:deployment>/chart/<int:chart>',
     delete)
)
