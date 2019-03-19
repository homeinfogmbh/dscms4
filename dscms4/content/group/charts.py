"""Management of charts in groups."""

from cmslib.functions.charts import get_chart
from cmslib.functions.group import get_group
from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_PATCHED
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.charts import BaseChart
from cmslib.orm.content.group import GroupBaseChart
from cmslib.orm.group import Group
from his import CUSTOMER, JSON_DATA, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


def list_gbc(gid):
    """Lists group base charts of the current
    customer with the respective group ID.
    """

    group_join = GroupBaseChart.group == Group.id
    bc_join = GroupBaseChart.base_chart == BaseChart.id
    return GroupBaseChart.select().join(
        Group, join_type='LEFT', on=group_join).join(
            BaseChart, join_type='LEFT', on=bc_join).where(
                (Group.customer == CUSTOMER.id) & (Group.id == gid)
                & (BaseChart.trashed == 0))


def get_gbc(gid, ident):
    """Returns the respective group base chart."""

    try:
        return GroupBaseChart.select().join(Group).where(
            (Group.customer == CUSTOMER.id) & (Group.id == gid)
            & (GroupBaseChart.id == ident)).get()
    except GroupBaseChart.DoesNotExist:
        raise NO_SUCH_CONTENT


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
    gbc = GroupBaseChart.from_json(JSON_DATA, group, base_chart)
    gbc.save()
    return CONTENT_ADDED.update(id=gbc.id)


@authenticated
@authorized('dscms4')
def patch(gid, ident):
    """Adds the chart to the respective terminal."""

    group_base_chart = get_gbc(gid, ident)
    group_base_chart.patch_json(JSON_DATA)
    group_base_chart.save()
    return CONTENT_PATCHED


@authenticated
@authorized('dscms4')
def delete(gid, ident):
    """Deletes the chart from the respective group."""

    group_base_chart = get_gbc(gid, ident)
    group_base_chart.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/group/<int:gid>/chart', get, 'list_group_charts'),
    ('POST', '/content/group/<int:gid>/chart/<int:ident>', add,
     'add_group_chart'),
    ('PATCH', '/content/group/<int:gid>/chart/<int:ident>', patch,
     'patch_group_chart'),
    ('DELETE', '/content/group/<int:gid>/chart/<int:ident>', delete,
     'delete_group_chart'))
