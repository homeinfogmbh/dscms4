"""Management of menus in deployments."""

from cmslib.functions.menu import get_menu
from cmslib.functions.deployment import get_deployment
from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_EXISTS
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.content.deployment import DeploymentMenu
from his import authenticated, authorized
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(deployment: int) -> JSON:
    """Returns a list of IDs of the menus in the respective deployment."""

    return JSON([
        deployment_menu.menu.id for deployment_menu
        in DeploymentMenu.select().where(
            DeploymentMenu.deployment == get_deployment(deployment))])


@authenticated
@authorized('dscms4')
def add(deployment: int, menu: int) -> JSONMessage:
    """Adds the menu to the respective deployment."""

    deployment = get_deployment(deployment)
    menu = get_menu(menu)

    try:
        DeploymentMenu.get(
            (DeploymentMenu.deployment == deployment)
            & (DeploymentMenu.menu == menu))
    except DeploymentMenu.DoesNotExist:
        deployment_menu = DeploymentMenu()
        deployment_menu.deployment = deployment
        deployment_menu.menu = menu
        deployment_menu.save()
        return CONTENT_ADDED

    return CONTENT_EXISTS


@authenticated
@authorized('dscms4')
def delete(deployment: int , menu: int) -> JSONMessage:
    """Deletes the menu from the respective deployment."""

    deployment = get_deployment(deployment)
    menu = get_menu(menu)

    try:
        deployment_menu = DeploymentMenu.get(
            (DeploymentMenu.deployment == deployment)
            & (DeploymentMenu.menu == menu))
    except DeploymentMenu.DoesNotExist:
        return NO_SUCH_CONTENT

    deployment_menu.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/deployment/<int:deployment>/menu', get),
    ('POST', '/content/deployment/<int:deployment>/menu/<int:menu>', add),
    ('DELETE', '/content/deployment/<int:deployment>/menu/<int:menu>', delete)
)
