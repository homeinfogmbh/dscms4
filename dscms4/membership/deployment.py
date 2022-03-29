"""Deployment memberships."""

from cmslib import DeploymentConfiguration, DeploymentBaseChart, DeploymentMenu
from his import CUSTOMER, authenticated, authorized
from hwdb import Deployment
from wsgilib import JSON


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_deployment_configurations() -> JSON:
    """List deployment configurations."""

    return JSON([
        dc.to_json() for dc in DeploymentConfiguration.select().join(
            Deployment
        ).where(
            Deployment.customer == CUSTOMER.id
        )
    ])


@authenticated
@authorized('dscms4')
def list_deployment_base_charts() -> JSON:
    """List deployment base charts."""

    return JSON([
        dbc.to_json() for dbc in DeploymentBaseChart.select().join(
            Deployment
        ).where(
            Deployment.customer == CUSTOMER.id
        )
    ])


@authenticated
@authorized('dscms4')
def list_deployment_menus() -> JSON:
    """List deployment menus."""

    return JSON([
        dm.to_json() for dm in DeploymentMenu.select().join(Deployment).where(
            Deployment.customer == CUSTOMER.id
        )
    ])


ROUTES = [
    (
        'GET', '/membership/deployment/configuration',
        list_deployment_configurations
    ),
    ('GET', '/membership/deployment/base-chart', list_deployment_base_charts),
    ('GET', '/membership/deployment/menu', list_deployment_menus)
]
