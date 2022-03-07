"""Digital signage deployment-related requests."""

from typing import Union

from cmslib import DeploymentPresentation
from cmslib import Settings
from cmslib import get_deployments
from cmslib import with_deployment
from his import CUSTOMER, authenticated, authorized
from hwdb import Deployment
from wsgilib import JSON, XML, get_bool


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists all deployments of the respective customer."""

    settings = Settings.for_customer(CUSTOMER.id)
    deployments = get_deployments(
        CUSTOMER.id,
        testing=settings.testing,
        content=(assoc := get_bool('assoc'))
    )

    if assoc:
        return JSON({
            deployment.id: deployment.to_json()
            for deployment in deployments
        })

    return JSON([
        deployment.to_json(address=True, systems=True)
        for deployment in deployments
    ])


@authenticated
@authorized('dscms4')
@with_deployment
def get(deployment: Deployment) -> JSON:
    """Returns the respective deployment."""

    return JSON(deployment.to_json(systems=True, cascade=1))


@authenticated
@authorized('dscms4')
@with_deployment
def get_presentation(deployment: Deployment) -> Union[JSON, XML]:
    """Returns the presentation for the respective deployment."""

    presentation = DeploymentPresentation(deployment)

    if get_bool('xml'):
        return XML(presentation.to_dom())

    return JSON(presentation.to_json())


ROUTES = [
    ('GET', '/deployment', list_),
    ('GET', '/deployment/<int:ident>', get),
    ('GET', '/deployment/<int:ident>/presentation', get_presentation)
]
