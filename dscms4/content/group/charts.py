"""Charts in groups."""

from dscms4.content.common import ContentInformation, get_charts
from dscms4.orm.content.group import GroupBaseChart


__all__ = [
    'base_charts',
    'accumulated_base_charts',
    'charts',
    'accumulated_charts']


def _base_charts(group):
    """Yields base charts of the respective group."""

    for group_base_chart in GroupBaseChart.select().where(
            GroupBaseChart.group == group):
        yield group_base_chart.base_chart


def base_charts(group):
    """Yields base charts of the respective group."""

    for base_chart in _base_charts(group):
        yield ContentInformation(group, base_chart)


def accumulated_base_charts(group):
    """Yields the accumulated base charts for this group."""

    yield from base_charts(group)
    parent = group.parent

    if parent:
        yield from accumulated_base_charts(parent)


def charts(group):
    """Yields charts of the group."""

    for chart in get_charts(_base_charts(group)):
        yield ContentInformation(group, chart)


def accumulated_charts(group):
    """Yields accumulated charts of the group."""

    yield from charts(group)
    parent = group.parent

    if parent:
        yield from accumulated_charts(parent)
