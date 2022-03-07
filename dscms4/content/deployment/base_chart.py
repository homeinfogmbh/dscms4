"""Management of base charts in deployments."""

from flask import request

from cmslib import DeploymentBaseChart
from cmslib import get_base_chart
from cmslib import get_deployment
from cmslib import get_deployment_base_chart
from cmslib import get_deployment_base_charts
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage, get_int, require_json


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists deployment <> base chart mappings."""

    return JSON([record.to_json() for record in get_deployment_base_charts(
        deployment=get_int('deployment'))])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the requested deployment <> base chart mapping."""

    return JSON(get_deployment_base_chart(ident).to_json())


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds a new deployment <> base chart mapping."""

    deployment = get_deployment(request.json.pop('deployment'), CUSTOMER.id)
    base_chart = get_base_chart(request.json.pop('baseChart'))
    record = DeploymentBaseChart.from_json(
        request.json, deployment, base_chart)
    record.save()
    return JSONMessage('Deployment base chart added.', id=record.id,
                       status=201)


@authenticated
@authorized('dscms4')
@require_json(dict)
def patch(ident: int) -> JSONMessage:
    """Patches a deployment <> base chart mapping, i.e. changes its index."""

    record = get_deployment_base_chart(ident)
    record.patch_json(request.json)
    record.save()
    return JSONMessage('Deployment base chart patched.', status=200)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes a deployment <> base chart mapping."""

    get_deployment_base_chart(ident).delete_instance()
    return JSONMessage('Deployment base chart deleted.', status=200)


ROUTES = [
    ('GET', '/content/deployment/base_chart', list_),
    ('GET', '/content/deployment/base_chart/<int:ident>', get),
    ('POST', '/content/deployment/base_chart', add),
    ('PATCH', '/content/deployment/base_chart/<int:ident>', patch),
    ('DELETE', '/content/deployment/base_chart/<int:ident>', delete)
]
