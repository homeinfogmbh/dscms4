"""Management of configurations in digital signage deployment."""

from flask import request

from cmslib import DeploymentConfiguration
from cmslib import get_configuration
from cmslib import get_deployment
from cmslib import get_deployment_configuration
from cmslib import get_deployment_configurations
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage, get_int, require_json


__all__ = ["ROUTES"]


@authenticated
@authorized("dscms4")
def list_() -> JSON:
    """Lists deployment <> configuration mappings."""

    return JSON(
        [
            record.to_json()
            for record in get_deployment_configurations(
                CUSTOMER.id, deployment=get_int("deployment")
            )
        ]
    )


@authenticated
@authorized("dscms4")
def get(ident: int) -> JSON:
    """Returns the respective deployment <> configuration mapping."""

    return JSON(get_deployment_configuration(ident, CUSTOMER.id).to_json())


@authenticated
@authorized("dscms4")
@require_json(dict)
def add() -> JSONMessage:
    """Adds a deployment <> configuration mapping."""

    deployment = get_deployment(request.json.pop("deployment"), CUSTOMER.id)
    configuration = get_configuration(request.json.pop("configuration"), CUSTOMER.id)
    record = DeploymentConfiguration(deployment=deployment, configuration=configuration)
    record.save()
    return JSONMessage("Deployment configuration added.", id=record.id, status=201)


@authenticated
@authorized("dscms4")
def delete(ident: int) -> JSONMessage:
    """Deleted a deployment <> configuration mapping."""

    get_deployment_configuration(ident, CUSTOMER.id).delete_instance()
    return JSONMessage("Deployment configuration deleted.", status=200)


ROUTES = [
    ("GET", "/content/deployment/configuration", list_),
    ("GET", "/content/deployment/configuration/<int:ident>", get),
    ("POST", "/content/deployment/configuration", add),
    ("DELETE", "/content/deployment/configuration/<int:ident>", delete),
]
