"""Management of base charts in deployments."""

from flask import request

from cmslib.functions.charts import get_base_chart
from cmslib.functions.content import get_deployment_base_chart
from cmslib.functions.content import get_deployment_base_charts
from cmslib.functions.deployment import get_deployment
from cmslib.orm.content.deployment import DeploymentBaseChart
from his import authenticated, authorized, require_json
from wsgilib import JSON, JSONMessage, get_bool


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists deployment base charts."""

    deployment = request.args.get('deployment')

    if deployment is not None:
        deployment = int(deployment)

    return JSON([dbc.to_json() for dbc in get_deployment_base_charts(
        deployment=deployment, trashed=get_bool('trashed', None))])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the requested deployment base chart."""

    return JSON(get_deployment_base_chart(ident).to_json())


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds the chart to the respective deployment."""

    deployment = get_deployment(request.json.pop('deployment'))
    base_chart = get_base_chart(request.json.pop('baseChart'))
    dbc = DeploymentBaseChart.from_json(request.json, deployment, base_chart)
    dbc.save()
    return JSONMessage('Deployment base chart added.', id=dbc.id, status=201)


@authenticated
@authorized('dscms4')
@require_json(dict)
def patch(ident: int) -> JSONMessage:
    """Adds the chart to the respective deployment."""

    dbc = get_deployment_base_chart(ident)
    dbc.patch_json(request.json)
    dbc.save()
    return JSONMessage('Deployment base chart patched.', status=200)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes the chart from the respective deployment."""

    get_deployment_base_chart(ident).delete_instance()
    return JSONMessage('Deployment base chart deleted.', status=200)


ROUTES = [
    ('GET', '/content/deployment/base_chart', list_),
    ('GET', '/content/deployment/base_chart/<int:ident>', get),
    ('POST', '/content/deployment/base_chart', add),
    ('PATCH', '/content/deployment/base_chart/<int:ident>', patch),
    ('DELETE', '/content/deployment/base_chart/<int:ident>', delete)
]
