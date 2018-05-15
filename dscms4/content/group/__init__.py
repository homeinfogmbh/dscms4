"""Content of groups."""

from dscms4.content.group.charts import charts
from dscms4.content.group.configuration import configurations
from dscms4.content.group.menu import menus
from dscms4.content.group.ticker import tickers


def content(group):
    """Yields the group's content."""

    yield from charts(group)
    yield from configurations(group)
    yield from menus(group)
    yield from tickers(group)


def accumulated_content(group):
    """Yields accumulated content of the group."""

    parent = group.parent

    if parent:
        yield from accumulated_content(parent)

    yield from content(group)
