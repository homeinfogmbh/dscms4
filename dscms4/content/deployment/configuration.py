"""Management of configurations in digital signage deployment."""

from cmslib.functions.configuration import get_configuration
from cmslib.functions.deployment import get_deployment
from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_EXISTS
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.content.deployment import DeploymentConfiguration
from his import authenticated, authorized
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


def get_deployment_configurations(deployment: int) -> ModelSelect:
    """Selects deployment configurations."""

    return DeploymentConfiguration.select(cascade=True).where(
        (DeploymentConfiguration.deployment == deployment)
        & (Configuration.customer == CUSTOMER.id)
        & (Deployment.customer == CUSTOMER.id))


@authenticated
@authorized('dscms4')
def get(deployment: int) -> JSON:
    """Returns a list of IDs of the configurations
    in the respective deployment.
    """

    return JSON([
        deployment_conf.configuration.id for deployment_conf
        in )])


@authenticated
@authorized('dscms4')
def add(deployment: int, configuration: int) -> JSONMessage:
    """Adds the configuration to the respective deployment."""

    deployment = get_deployment(deployment)
    configuration = get_configuration(configuration)

    try:
        DeploymentConfiguration.get(
            (DeploymentConfiguration.deployment == deployment)
            & (DeploymentConfiguration.configuration == configuration))
    except DeploymentConfiguration.DoesNotExist:
        deployment_conf = DeploymentConfiguration()
        deployment_conf.deployment = deployment
        deployment_conf.configuration = configuration
        deployment_conf.save()
        return CONTENT_ADDED

    return CONTENT_EXISTS


@authenticated
@authorized('dscms4')
def delete(deployment: int, configuration: int) -> JSONMessage:
    """Deletes the configuration from the respective deployment."""

    deployment = get_deployment(deployment)
    configuration = get_configuration(configuration)

    try:
        deployment_conf = DeploymentConfiguration.get(
            (DeploymentConfiguration.deployment == deployment)
            & (DeploymentConfiguration.configuration == configuration))
    except DeploymentConfiguration.DoesNotExist:
        return NO_SUCH_CONTENT

    deployment_conf.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/deployment/<int:deployment>/configuration', get),
    ('POST',
     '/content/deployment/<int:deployment>/configuration/<int:configuration>',
     add),
    ('DELETE',
     '/content/deployment/<int:deployment>/configuration/<int:configuration>',
     delete)
)
