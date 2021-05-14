"""Digital signage deployment-related requests."""

from sys import stdout
from typing import Iterator, Union

from cmslib import BaseChart
from cmslib import DeploymentBaseChart
from cmslib import DeploymentConfiguration
from cmslib import DeploymentMenu
from cmslib import DeploymentPresentation
from cmslib import Settings
from cmslib import get_deployments
from cmslib import get_trashed
from cmslib import with_deployment
from functoolsplus import timeit
from his import CUSTOMER, authenticated, authorized
from hwdb import Deployment
from wsgilib import Browser, JSON, XML, get_bool


__all__ = ['ROUTES']


BROWSER = Browser()


@timeit(file=stdout, flush=True)
def _jsonify(deployment: Deployment) -> dict:
    """Returns a JSON representation of the
    deployment with address and system IDs.
    """

    json = deployment.to_json(cascade=1, systems=True, skip={'customer'})

    try:
        content = {
            'charts': [
                dbc.to_json() for dbc in deployment.deploymentbasechart
            ],
            'configurations': [
                dc.to_json() for dc in deployment.deploymentconfiguration
            ],
            'menus': [dm.to_json() for dm in deployment.deploymentmenu]
        }
    except AttributeError:
        return json

    return {'deployment': json, 'content': content}


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists all deployments of the respective customer."""

    deployments = get_deployments(content=get_bool('assoc'))
    settings = Settings.for_customer(CUSTOMER.id)

    if not settings.testing:
        deployments = deployments.where(Deployment.testing == 0)

    if BROWSER.wanted:
        if BROWSER.info:
            return BROWSER.pages(deployments).to_json()

        deployments = BROWSER.browse(deployments)
        return JSON([_jsonify(deployment) for deployment in deployments])

    if get_bool('assoc'):
        return JSON({
            deployment.id: _jsonify(deployment) for deployment in deployments
        })

    return JSON([_jsonify(deployment) for deployment in deployments])


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


class DeploymentContent:
    """Represents content of a deployment."""

    def __init__(self, deployment: Deployment):
        """Sets the deployment."""
        self.deployment = deployment

    @property
    def charts(self) -> Iterator[dict]:
        """Yields the deployment's charts."""
        for dbc in DeploymentBaseChart.select().join(BaseChart).where(
                (DeploymentBaseChart.deployment == self.deployment)
                & get_trashed()):
            yield dbc.to_json()

    @property
    def configurations(self) -> Iterator[dict]:
        """Yields the deployment's configurations."""
        for deployment_config in DeploymentConfiguration.select().where(
                DeploymentConfiguration.deployment == self.deployment):
            yield deployment_config.to_json()

    @property
    def menus(self) -> Iterator[dict]:
        """Yields the deployment's menus."""
        for deployment_menu in DeploymentMenu.select().where(
                DeploymentMenu.deployment == self.deployment):
            yield deployment_menu.to_json()

    def content(self) -> dict:
        """Returns content."""
        return {
            'charts': list(self.charts),
            'configurations': list(self.configurations),
            'menus': list(self.menus)
        }

    def to_json(self) -> dict:
        """Returns the deployment and its content as a JSON-ish dict."""
        return {
            'deployment': _jsonify(self.deployment),
            'content': self.content()
        }


ROUTES = [
    ('GET', '/deployment', list_),
    ('GET', '/deployment/<int:ident>', get),
    ('GET', '/deployment/<int:ident>/presentation', get_presentation)
]
