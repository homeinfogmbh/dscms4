"""Management of charts in groups."""

from peewee import DoesNotExist

from wsgilib import JSON

from dscms4.messages.content.group import NoSuchGroupChart, ChartAddedToGroup,\
    ChartAlreadyInGroup, ChartDeletedFromGroup
from dscms4.orm.content.group import GroupBaseChart
from dscms4.wsgi.chart import _get_chart
from dscms4.wsgi.group import _get_group

__all__ = ['get_group_charts', 'add_group_chart', 'delete_group_chart']


def get_group_charts(gid):
    """Returns a list of IDs of the charts in the respective group."""

    return JSON([gbc.chart.id for gbc in GroupBaseChart.select().where(
        GroupBaseChart.group == _get_group(gid))])


def add_group_chart(gid, ident):
    """Adds the chart to the respective group."""

    group = _get_group(gid)
    chart = _get_chart(ident)

    try:
        GroupBaseChart.get(
            (GroupBaseChart.group == group) & (GroupBaseChart.chart == chart))
    except DoesNotExist:
        gbc = GroupBaseChart()
        gbc.group = group
        gbc.chart = chart
        gbc.save()
        return ChartAddedToGroup()

    return ChartAlreadyInGroup()


def delete_group_chart(gid, ident):
    """Deletes the chart from the respective group."""

    try:
        group_chart = GroupBaseChart.get(
            (GroupBaseChart.group == _get_group(gid))
            & (GroupBaseChart.id == ident))
    except DoesNotExist:
        raise NoSuchGroupChart()

    group_chart.delete_instance()
    return ChartDeletedFromGroup()
