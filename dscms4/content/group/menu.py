"""Group menus content."""

from dscms4.content.common import ContentInformation
from dscms4.orm.content.group import GroupMenu

__all__ = ['menus', 'accumulated_menus']


def menus(group):
    """Yields menus of the respective group."""

    for group_menu in GroupMenu.select().where(GroupMenu.group == group):
        yield ContentInformation(group, group_menu.menu)


def accumulated_menus(group):
    """Yields accumulated group menus."""

    yield from menus(group)
    parent = group.parent

    if parent:
        yield from accumulated_menus(parent)
