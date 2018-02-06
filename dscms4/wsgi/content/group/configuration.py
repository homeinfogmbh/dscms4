"""Management of configurations in groups."""

from wsgilib import JSON

from dscms4.messages.content import NoSuchContent, ContentAdded, \
    ContentExists, ContentDeleted
from dscms4.orm.content.group import GroupConfiguration
from dscms4.wsgi.configuration import _get_configuration
from dscms4.wsgi.group import _get_group

__all__ = ['ROUTES']


def get(gid):
    """Returns a list of IDs of the configurations in the respective group."""

    return JSON([
        group_configuration.configuration.id for group_configuration
        in GroupConfiguration.select().where(
            GroupConfiguration.group == _get_group(gid))])


def add(gid, ident):
    """Adds the configuration to the respective group."""

    group = _get_group(gid)
    configuration = _get_configuration(ident)

    try:
        GroupConfiguration.get(
            (GroupConfiguration.group == group)
            & (GroupConfiguration.configuration == configuration))
    except GroupConfiguration.DoesNotExist:
        group_configuration = GroupConfiguration()
        group_configuration.group = group
        group_configuration.configuration = configuration
        group_configuration.save()
        return ContentAdded()

    return ContentExists()


def delete(gid, ident):
    """Deletes the configuration from the respective group."""

    try:
        group_configuration = GroupConfiguration.get(
            (GroupConfiguration.group == _get_group(gid))
            & (GroupConfiguration.id == ident))
    except GroupConfiguration.DoesNotExist:
        raise NoSuchContent()

    group_configuration.delete_instance()
    return ContentDeleted()


ROUTES = (
    ('GET', '/content/group/<int:gid>/configuration', get,
     'list_group_configurations'),
    ('POST', '/content/group/<int:gid>/configuration', add,
     'add_group_configuration'),
    ('DELETE', '/content/group/<int:gid>/configuration/<int:ident>', delete,
     'delete_group_configuration'))
