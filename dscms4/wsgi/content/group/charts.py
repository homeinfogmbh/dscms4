"""Management of charts in groups."""

from his import authenticated, authorized
from wsgilib import JSON

from dscms4.messages.content import NoSuchContent, ContentAdded, \
    ContentExists, ContentDeleted
from dscms4.orm.content.group import GroupBaseChart
from dscms4.orm.util import chart_of
from dscms4.wsgi.charts import get_chart
from dscms4.wsgi.group import get_group

__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(gid):
    """Returns a list of IDs of the charts in the respective group."""

    return JSON([
        chart_of(gbc.base_chart).to_dict(brief=True)
        for gbc in GroupBaseChart.select().where(
            GroupBaseChart.group == get_group(gid))])


@authenticated
@authorized('dscms4')
def add(gid, ident):
    """Adds the chart to the respective group."""

    group = get_group(gid)
    base_chart = get_chart(ident).base

    try:
        GroupBaseChart.get(
            (GroupBaseChart.group == group)
            & (GroupBaseChart.base_chart == base_chart))
    except GroupBaseChart.DoesNotExist:
        gbc = GroupBaseChart()
        gbc.group = group
        gbc.base_chart = base_chart
        gbc.save()
        return ContentAdded()

    return ContentExists()


@authenticated
@authorized('dscms4')
def delete(gid, ident):
    """Deletes the chart from the respective group."""

    group = get_group(gid)
    base_chart = get_chart(ident).base

    try:
        group_chart = GroupBaseChart.get(
            (GroupBaseChart.group == group)
            & (GroupBaseChart.base_chart == base_chart))
    except GroupBaseChart.DoesNotExist:
        raise NoSuchContent()

    group_chart.delete_instance()
    return ContentDeleted()


ROUTES = (
    ('GET', '/content/group/<int:gid>/chart', get, 'list_group_charts'),
    ('POST', '/content/group/<int:gid>/chart/<int:ident>', add,
     'add_group_chart'),
    ('DELETE', '/content/group/<int:gid>/chart/<int:ident>', delete,
     'delete_group_chart'))
