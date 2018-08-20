"""Management of charts in groups."""

from his import authenticated, authorized
from wsgilib import JSON

from dscms4.messages.content import NoSuchContent, ContentAdded, \
    ContentDeleted
from dscms4.messages.group import NoSuchGroup
from dscms4.orm.content.group import GroupBaseChart
from dscms4.orm.group import Group
from dscms4.wsgi.charts import get_chart


__all__ = ['ROUTES']


def _get_gbc(gid, ident):
    """Returns the respective group base chart."""

    try:
        group = Group.cget(Group.id == gid)
    except Group.DoesNotExist:
        raise NoSuchGroup()

    try:
        return GroupBaseChart.get().where(
            (GroupBaseChart.id == ident) & (GroupBaseChart.group == group))
    except GroupBaseChart.DoesNotExist:
        raise NoSuchContent()


@authenticated
@authorized('dscms4')
def get(gid):
    """Returns a list of IDs of the charts in the respective group."""

    try:
        group = Group.cget(Group.id == gid)
    except Group.DoesNotExist:
        return NoSuchGroup()

    return JSON([
        gbc.to_dict() for gbc in GroupBaseChart.select().where(
            GroupBaseChart.group == group)])


@authenticated
@authorized('dscms4')
def add(gid, ident):
    """Adds the chart to the respective group."""

    try:
        group = Group.cget(Group.id == gid)
    except Group.DoesNotExist:
        return NoSuchGroup()

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

    _get_gbc(gid, ident).delete_instance()
    return ContentDeleted()


ROUTES = (
    ('GET', '/content/group/<int:gid>/chart', get, 'list_group_charts'),
    ('POST', '/content/group/<int:gid>/chart/<int:ident>', add,
     'add_group_chart'),
    ('DELETE', '/content/group/<int:gid>/chart/<int:ident>', delete,
     'delete_group_chart'))
