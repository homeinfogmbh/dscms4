"""Management of configurations in digital signage deployment."""

from flask import request

from cmslib.functions.configuration import get_configuration
from cmslib.functions.content import get_deployment_configuration
from cmslib.functions.content import get_deployment_configurations
from cmslib.functions.deployment import get_deployment
from cmslib.orm.content.deployment import DeploymentConfiguration
from his import authenticated, authorized, require_json
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists deployment configurations."""

    deployment = request.args.get('deployment')

    if deployment is not None:
        deployment = int(deployment)

    return JSON([record.to_json() for record in get_deployment_configurations(
        deployment=deployment)])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the respective deployment configuration."""

    return JSON(get_deployment_configuration(ident).to_json())


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds the configuration to the respective deployment."""

    deployment = get_deployment(request.json.pop('deployment'))
    configuration = get_configuration(request.json.pop('configuration'))
    record = DeploymentConfiguration(
        deployment=deployment, configuration=configuration)
    record.save()
    return JSONMessage(
        'Deployment configuration added.', id=record.id, status=201)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes the configuration from the respective deployment."""

    get_deployment_configuration(ident).delete_instance()
    return JSONMessage('Deployment configuration deleted.', status=200)


ROUTES = [
    ('GET', '/content/deployment/configuration', list_),
    ('GET', '/content/deployment/configuration/<int:ident>', get),
    ('POST', '/content/deployment/configuration', add),
    ('DELETE', '/content/deployment/configuration/<int:ident>', delete)
]
