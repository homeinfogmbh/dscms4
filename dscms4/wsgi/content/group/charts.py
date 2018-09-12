"""Management of charts in groups."""

from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON

from dscms4.messages.content import NoSuchContent, ContentAdded, \
    ContentDeleted
from dscms4.orm.charts import BaseChart
from dscms4.orm.content.group import GroupBaseChart
from dscms4.orm.group import Group
from dscms4.wsgi.charts import get_chart
from dscms4.wsgi.group.group import get_group


__all__ = ['ROUTES']


def get_gbc(gid, ident):
    """Returns the respective group base chart."""

    group = get_group(gid)

    try:
        return GroupBaseChart.get(
            (GroupBaseChart.id == ident) & (GroupBaseChart.group == group))
    except GroupBaseChart.DoesNotExist:
        raise NoSuchContent()


def list_gbc(gid):
    """Lists group base charts of the current
    customer with the respective group ID.
    """

    return GroupBaseChart.select().join(Group).join(
        BaseChart, on=GroupBaseChart.base_chart == BaseChart.id).where(
            (Group.customer == CUSTOMER.id) & (Group.id == gid)
            & (BaseChart.trashed == 0)).get()


@authenticated
@authorized('dscms4')
def get(gid):
    """Returns a list of IDs of the charts in the respective group."""

    return JSON([gbc.to_json() for gbc in list_gbc(gid)])


@authenticated
@authorized('dscms4')
def add(gid, ident):
    """Adds the chart to the respective group."""

    group = get_group(gid)
    base_chart = get_chart(ident).base
    gbc = GroupBaseChart()
    gbc.group = group
    gbc.base_chart = base_chart
    gbc.save()
    return ContentAdded(id=gbc.id)


@authenticated
@authorized('dscms4')
def delete(gid, ident):
    """Deletes the chart from the respective group."""

    group_base_chart = get_gbc(gid, ident)
    group_base_chart.delete_instance()
    return ContentDeleted()


ROUTES = (
    ('GET', '/content/group/<int:gid>/chart', get, 'list_group_charts'),
    ('POST', '/content/group/<int:gid>/chart/<int:ident>', add,
     'add_group_chart'),
    ('DELETE', '/content/group/<int:gid>/chart/<int:ident>', delete,
     'delete_group_chart'))
