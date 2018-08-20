"""Group configuration content."""

from dscms4.content.common import ContentInformation
from dscms4.content.exceptions import NoConfigurationFound
from dscms4.orm.content.group import GroupConfiguration


__all__ = ['configurations', 'first_configuration']


def configurations(group):
    """Yields the group's configurations."""

    for group_configuration in GroupConfiguration.select().where(
            GroupConfiguration.group == group):
        yield ContentInformation(group, group_configuration.configuration)


def first_configuration(group):
    """Yields the accumulated configurations for this group."""

    for _, configuration in configurations(group):
        return configuration

    parent = group.parent

    if parent:
        return first_configuration(parent)

    raise NoConfigurationFound()
