"""Digital signage deployment-related requests."""

from typing import Iterable, Iterator, Union

from flask import request
from peewee import Expression

from cmslib.exceptions import AmbiguousConfigurationsError
from cmslib.exceptions import NoConfigurationFound
from cmslib.functions.deployment import with_deployment
from cmslib.messages.presentation import NO_CONFIGURATION_ASSIGNED
from cmslib.messages.presentation import AMBIGUOUS_CONFIGURATIONS
from cmslib.orm.charts import BaseChart
from cmslib.orm.content.deployment import DeploymentBaseChart
from cmslib.orm.content.deployment import DeploymentConfiguration
from cmslib.orm.content.deployment import DeploymentMenu
from cmslib.orm.settings import Settings
from cmslib.presentation.deployment import Presentation
from his import CUSTOMER, authenticated, authorized
from hwdb import Deployment
from mdb import Address
from wsgilib import Browser, JSON, JSONMessage, XML


__all__ = ['ROUTES']


BROWSER = Browser()


def _get_deployments(expression: Expression) -> Iterable[Deployment]:
    """Yields deployments with address and system IDs."""

    address_join = Deployment.address == Address.id
    return Deployment.select(Deployment, Address).join(
        Address, on=address_join).where(expression)


def _jsonify(deployment: Deployment) -> dict:
    """Returns a JSON representation of the
    deployment with address and system IDs.
    """

    return deployment.to_json(cascade=1, systems=True, skip={'customer'})


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists all deployments of the respective customer."""

    expression = Deployment.customer == CUSTOMER.id
    settings = Settings.for_customer(CUSTOMER.id)

    if not settings.testing:
        expression &= Deployment.testing == 0

    deployments = _get_deployments(expression)

    if BROWSER.wanted:
        if BROWSER.info:
            return BROWSER.pages(deployments).to_json()

        deployments = BROWSER.browse(deployments)
        return JSON([_jsonify(deployment) for deployment in deployments])

    if 'assoc' in request.args:
        mapping = {
            deployment.id: DeploymentContent(deployment).to_json()
            for deployment in deployments}
        return JSON(mapping)

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
def get_presentation(deployment: Deployment) -> Union[JSON, JSONMessage, XML]:
    """Returns the presentation for the respective deployment."""

    presentation = Presentation(deployment)

    try:
        request.args['xml']
    except KeyError:
        return JSON(presentation.to_json())

    try:
        presentation_dom = presentation.to_dom()
    except AmbiguousConfigurationsError:
        return AMBIGUOUS_CONFIGURATIONS
    except NoConfigurationFound:
        return NO_CONFIGURATION_ASSIGNED

    return XML(presentation_dom)


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
                & (BaseChart.trashed == 0)):
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


ROUTES = (
    ('GET', '/deployment', list_),
    ('GET', '/deployment/<int:ident>', get),
    ('GET', '/deployment/<int:ident>/presentation', get_presentation)
)
