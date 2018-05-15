"""Group configuration content."""

from dscms4.content.common import ContentInformation
from dscms4.orm.content.group import GroupConfiguration

__all__ = ['configurations', 'accumulated_configurations']


def configurations(group):
    """Yields the group's configurations."""

    for group_configuration in GroupConfiguration.select().where(
            GroupConfiguration.group == group):
        yield ContentInformation(group, group_configuration.configuration)


def accumulated_configurations(group):
    """Yields the accumulated configurations for this group."""

    yield from configurations(group)
    parent = group.parent

    if parent:
        yield from accumulated_configurations(parent)
