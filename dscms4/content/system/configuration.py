"""Management of configurations in digital signage systems."""

from cmslib.functions.configuration import get_configuration
from cmslib.functions.system import get_system
from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_EXISTS
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.content.system import SystemConfiguration
from his import authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(system):
    """Returns a list of IDs of the configurations
    in the respective system.
    """

    return JSON([
        system_configuration.configuration.id for system_configuration
        in SystemConfiguration.select().where(
            SystemConfiguration.system == get_system(system))])


@authenticated
@authorized('dscms4')
def add(system, configuration):
    """Adds the configuration to the respective system."""

    system = get_system(system)
    configuration = get_configuration(configuration)

    try:
        SystemConfiguration.get(
            (SystemConfiguration.system == system)
            & (SystemConfiguration.configuration == configuration))
    except SystemConfiguration.DoesNotExist:
        system_configuration = SystemConfiguration()
        system_configuration.system = system
        system_configuration.configuration = configuration
        system_configuration.save()
        return CONTENT_ADDED

    return CONTENT_EXISTS


@authenticated
@authorized('dscms4')
def delete(system, configuration):
    """Deletes the configuration from the respective system."""

    system = get_system(system)
    configuration = get_configuration(configuration)

    try:
        system_configuration = SystemConfiguration.get(
            (SystemConfiguration.system == system)
            & (SystemConfiguration.configuration == configuration))
    except SystemConfiguration.DoesNotExist:
        raise NO_SUCH_CONTENT

    system_configuration.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/system/<int:system>/configuration', get),
    ('POST', '/content/system/<int:system>/configuration/<int:configuration>',
     add),
    ('DELETE',
     '/content/system/<int:system>/configuration/<int:configuration>', delete)
)
