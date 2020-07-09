"""Management of charts in deployments."""

from cmslib.functions.charts import get_chart
from cmslib.functions.deployment import get_deployment
from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_PATCHED
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.charts import BaseChart
from cmslib.orm.content.deployment import DeploymentBaseChart
from his import CUSTOMER, JSON_DATA, authenticated, authorized
from hwdb import Deployment
from wsgilib import JSON


__all__ = ['ROUTES']


def list_dbc(ident):
    """Yields the deployment base charts of the
    current customer for the respective termianl.
    """

    return DeploymentBaseChart.select().join(Deployment).join(BaseChart).where(
        (Deployment.id == ident)
        & (Deployment.customer == CUSTOMER.id)
        & (BaseChart.trashed == 0))


def get_dbc(deployment, ident):
    """Returns the respective deployment base chart."""

    try:
        return DeploymentBaseChart.select().join(Deployment).where(
            (DeploymentBaseChart.id == ident)
            & (Deployment.id == deployment)
            & (Deployment.customer == CUSTOMER.id)).get()
    except DeploymentBaseChart.DoesNotExist:
        raise NO_SUCH_CONTENT


@authenticated
@authorized('dscms4')
def get(deployment):
    """Returns a list of IDs of the charts in the respective deployment."""

    return JSON([dbc.to_json() for dbc in list_dbc(deployment)])


@authenticated
@authorized('dscms4')
def add(deployment, chart):
    """Adds the chart to the respective deployment."""

    deployment = get_deployment(deployment)
    base_chart = get_chart(chart).base
    dbc = DeploymentBaseChart.from_json(JSON_DATA, deployment, base_chart)
    dbc.save()
    return CONTENT_ADDED.update(id=dbc.id)


@authenticated
@authorized('dscms4')
def patch(deployment, chart):
    """Adds the chart to the respective deployment."""

    dbc = get_dbc(deployment, chart)
    dbc.patch_json(JSON_DATA)
    dbc.save()
    return CONTENT_PATCHED


@authenticated
@authorized('dscms4')
def delete(deployment, chart):
    """Deletes the chart from the respective deployment."""

    dbc = get_dbc(deployment, chart)
    dbc.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/deployment/<int:deployment>/chart', get),
    ('POST', '/content/deployment/<int:deployment>/chart/<int:chart>', add),
    ('PATCH', '/content/deployment/<int:deployment>/chart/<int:chart>', patch),
    ('DELETE', '/content/deployment/<int:deployment>/chart/<int:chart>',
     delete)
)
