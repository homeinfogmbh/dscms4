"""Management of charts in groups."""

from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON

from dscms4.messages.content import NoSuchContent, ContentAdded, \
    ContentDeleted
from dscms4.orm.content.group import Group, GroupBaseChart
from dscms4.wsgi.charts import get_chart
from dscms4.wsgi.group import get_group

__all__ = ['ROUTES']


def _get_gbc(gid, ident):
    """Returns the respective group base chart."""

    try:
        return GroupBaseChart.select().join(Group).where(
            (GroupBaseChart.id == ident)
            & (Group.customer == CUSTOMER.id)
            & (Group.id == gid)).get()
    except GroupBaseChart.DoesNotExist:
        raise NoSuchContent()


@authenticated
@authorized('dscms4')
def get(gid):
    """Returns a list of IDs of the charts in the respective group."""

    return JSON([
        gbc.to_dict() for gbc in GroupBaseChart.select().where(
            GroupBaseChart.group == get_group(gid))])


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

    _get_gbc(gid, ident).delete_instance()
    return ContentDeleted()


ROUTES = (
    ('GET', '/content/group/<int:gid>/chart', get, 'list_group_charts'),
    ('POST', '/content/group/<int:gid>/chart/<int:ident>', add,
     'add_group_chart'),
    ('DELETE', '/content/group/<int:gid>/chart/<int:ident>', delete,
     'delete_group_chart'))
