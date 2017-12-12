"""Management of configurations in groups."""

from peewee import DoesNotExist

from wsgilib import JSON

from dscms4.messages.content.group import NoSuchGroupConfiguration, \
    ConfigurationAddedToGroup, ConfigurationAlreadyInGroup, \
    ConfigurationDeletedFromGroup
from dscms4.orm.content.group import GroupConfiguration
from dscms4.wsgi.configuration import _get_configuration
from dscms4.wsgi.group import _get_group

__all__ = [
    'get_group_configurations',
    'add_group_configuration',
    'delete_group_configuration']


def get_group_configurations(gid):
    """Returns a list of IDs of the configurations in the respective group."""

    return JSON([
        group_configuration.configuration.id for group_configuration
        in GroupConfiguration.select().where(
            GroupConfiguration.group == _get_group(gid))])


def add_group_configuration(gid, ident):
    """Adds the configuration to the respective group."""

    group = _get_group(gid)
    configuration = _get_configuration(ident)

    try:
        GroupConfiguration.get(
            (GroupConfiguration.group == group)
            & (GroupConfiguration.configuration == configuration))
    except DoesNotExist:
        group_configuration = GroupConfiguration()
        group_configuration.group = group
        group_configuration.configuration = configuration
        group_configuration.save()
        return ConfigurationAddedToGroup()

    return ConfigurationAlreadyInGroup()


def delete_group_configuration(gid, ident):
    """Deletes the configuration from the respective group."""

    try:
        group_configuration = GroupConfiguration.get(
            (GroupConfiguration.group == _get_group(gid))
            & (GroupConfiguration.id == ident))
    except DoesNotExist:
        raise NoSuchGroupConfiguration()

    group_configuration.delete_instance()
    return ConfigurationDeletedFromGroup()
