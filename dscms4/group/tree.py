"""Groups tree endpoint."""

from cmslib.orm.charts import BaseChart
from cmslib.orm.content.group import GroupBaseChart
from cmslib.orm.content.group import GroupConfiguration
from cmslib.orm.content.group import GroupMenu
from cmslib.orm.group import Group, GroupMemberTerminal
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON

from dscms4.group.group import get_group


__all__ = ['ROUTES']


def get_groups_tree():
    """Returns the management tree."""

    root_groups = Group.select().where(
        (Group.customer == CUSTOMER.id) & (Group.parent >> None))

    for root_group in root_groups:
        yield GroupContent(root_group)


@authenticated
@authorized('dscms4')
def groups_tree():
    """Lists the groups."""

    return JSON([group.to_json() for group in get_groups_tree()])


@authenticated
@authorized('dscms4')
def groups_subtree(gid):
    """Lists the groups."""

    group_content = GroupContent(get_group(gid))
    return JSON(group_content.to_json(recursive=False))


class GroupContent:
    """Represents content of a group."""

    def __init__(self, group):
        """Sets the respective group."""
        self.group = group

    @property
    def children(self):
        """Yields children of this group."""
        for group in Group.select().where(Group.parent == self.group):
            yield GroupContent(group)

    @property
    def charts(self):
        """Yields the group's charts."""
        bc_join = GroupBaseChart.base_chart == BaseChart.id

        for group_base_chart in GroupBaseChart.select().join(
                BaseChart, join_type='LEFT', on=bc_join).where(
                    (GroupBaseChart.group == self.group)
                    & (BaseChart.trashed == 0)):
            yield group_base_chart.to_json()

    @property
    def configurations(self):
        """Yields the group's configurations."""
        for group_configuration in GroupConfiguration.select().where(
                GroupConfiguration.group == self.group):
            yield group_configuration.to_json()

    @property
    def menus(self):
        """Yields the group's menus."""
        for group_menu in GroupMenu.select().where(
                GroupMenu.group == self.group):
            yield group_menu.to_json()

    @property
    def terminals(self):
        """Yields the group's terminals."""
        for group_member_terminal in GroupMemberTerminal.select().where(
                GroupMemberTerminal.group == self.group):
            yield group_member_terminal.to_json()

    @property
    def content_and_terminals(self):
        """Returns content and terminals."""
        content = {
            'charts': list(self.charts),
            'configurations': list(self.configurations),
            'menus': list(self.menus)}
        return (content, list(self.terminals))

    def to_json(self, recursive=True):
        """Recursively converts the group content into a JSON-ish dict."""
        json = self.group.to_json(parent=False, skip=('customer',))

        if recursive:
            children = [
                group.to_json(recursive=True) for group in self.children]
        else:
            children = [
                group.group.to_json(parent=False, skip=('customer',))
                for group in self.children]

        json['children'] = children
        json['content'], terminals = self.content_and_terminals
        json['members'] = {'terminals': terminals}
        return json


ROUTES = (
    ('GET', '/grouptree', groups_tree, 'groups_tree'),
    ('GET', '/grouptree/<int:gid>', groups_subtree, 'groups_subtree'))
