"""Group content resolver."""

from dscms4.content.group.charts import charts
from dscms4.content.group.configuration import configurations
from dscms4.content.group.menu import menus


def content(group):
    """Yields the group's content."""

    yield from charts(group)
    yield from configurations(group)
    yield from menus(group)


def accumulated_content(group):
    """Yields accumulated content of the group."""

    parent = group.parent

    if parent:
        yield from accumulated_content(parent)

    yield from content(group)
