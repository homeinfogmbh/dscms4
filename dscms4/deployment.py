"""Digital signage deployment-related requests."""

from typing import Union

from cmslib import DATABASE
from cmslib import DeploymentPresentation
from cmslib import Settings
from cmslib import get_deployments
from cmslib import with_deployment
from his import CUSTOMER, authenticated, authorized
from hwdb import Deployment
from wsgilib import Browser, JSON, XML, get_bool


__all__ = ['ROUTES']


BROWSER = Browser()


def jsonify(deployment: Deployment) -> dict:
    """Returns a JSON representation of the
    deployment with address and system IDs.
    """

    json = deployment.to_json(cascade=1, systems=True, skip={'customer'})
    content = {}

    try:
        base_charts = deployment.deploymentbasechart_set
    except AttributeError:
        pass
    else:
        content['charts'] = [dbc.to_json() for dbc in base_charts]

    try:
        configurations = deployment.deploymentconfiguration_set
    except AttributeError:
        pass
    else:
        content['configurations'] = [dc.to_json() for dc in configurations]

    try:
        menus = deployment.deploymentmenu_set
    except AttributeError:
        pass
    else:
        content['menus'] = [dm.to_json() for dm in menus]

    if content:
        return {'deployment': json, 'content': content}

    return json


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists all deployments of the respective customer."""

    deployments = get_deployments(content=get_bool('assoc'))
    settings = Settings.for_customer(CUSTOMER.id)

    if not settings.testing:
        deployments = deployments.where(Deployment.testing == 0)

    # Run query as dscms4 database user.
    deployments = deployments.execute(DATABASE)

    if BROWSER.wanted:
        if BROWSER.info:
            return BROWSER.pages(deployments).to_json()

        deployments = BROWSER.browse(deployments)
        return JSON([jsonify(deployment) for deployment in deployments])

    if get_bool('assoc'):
        return JSON({
            deployment.id: jsonify(deployment) for deployment in deployments
        })

    return JSON([jsonify(deployment) for deployment in deployments])


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
