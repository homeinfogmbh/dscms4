"""Management of configurations in groups."""

from cmslib.functions.configuration import get_configuration
from cmslib.functions.group import get_group
from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_EXISTS
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.content.group import GroupConfiguration
from his import authenticated, authorized
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(gid: int) -> JSON:
    """Returns a list of IDs of the configurations in the respective group."""

    group = get_group(gid)

    return JSON([
        group_configuration.configuration.id for group_configuration
        in GroupConfiguration.select().where(
            GroupConfiguration.group == group)])


@authenticated
@authorized('dscms4')
def add(gid: int, ident: int) -> JSONMessage:
    """Adds the configuration to the respective group."""

    group = get_group(gid)
    configuration = get_configuration(ident)

    try:
        GroupConfiguration.get(
            (GroupConfiguration.group == group)
            & (GroupConfiguration.configuration == configuration))
    except GroupConfiguration.DoesNotExist:
        group_configuration = GroupConfiguration()
        group_configuration.group = group
        group_configuration.configuration = configuration
        group_configuration.save()
        return CONTENT_ADDED

    return CONTENT_EXISTS


@authenticated
@authorized('dscms4')
def delete(gid: int, ident: int) -> JSONMessage:
    """Deletes the configuration from the respective group."""

    group = get_group(gid)
    configuration = get_configuration(ident)

    try:
        group_configuration = GroupConfiguration.get(
            (GroupConfiguration.group == group)
            & (GroupConfiguration.configuration == configuration))
    except GroupConfiguration.DoesNotExist:
        return NO_SUCH_CONTENT

    group_configuration.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/group/<int:gid>/configuration', get),
    ('POST', '/content/group/<int:gid>/configuration/<int:ident>', add),
    ('DELETE', '/content/group/<int:gid>/configuration/<int:ident>', delete)
)
