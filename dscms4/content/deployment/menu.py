"""Management of menus in deployments."""

from flask import request

from cmslib import DeploymentMenu
from cmslib import get_deployment
from cmslib import get_deployment_menu
from cmslib import get_deployment_menus
from cmslib import get_menu
from his import authenticated, authorized, require_json
from wsgilib import JSON, JSONMessage, get_int


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists deployment <> menu mappings."""

    return JSON([record.to_json() for record in get_deployment_menus(
        deployment=get_int('deployment'))])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the requested deployment <> menu mapping."""

    return JSON(get_deployment_menu(ident).to_json())


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds a deployment <> base chart mapping."""

    deployment = get_deployment(request.json.pop('deployment'))
    menu = get_menu(request.json.pop('menu'))
    record = DeploymentMenu(deployment=deployment, menu=menu)
    record.save()
    return JSONMessage('Deplyoment menu added.', id=record.id, status=201)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes a deployment <> base chart mapping."""

    get_deployment_menu(ident).delete_instance()
    return JSONMessage('Deployment menu deleted.', status=200)


ROUTES = [
    ('GET', '/content/deployment/menu/', list_),
    ('GET', '/content/deployment/menu/<int:ident>', get),
    ('POST', '/content/deployment/menu', add),
    ('DELETE', '/content/deployment/menu/<int:ident>', delete)
]
