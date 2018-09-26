"""Groups tree endpoint."""

from logging import getLogger

from flask import request

from his import CUSTOMER
from peeweeplus import async_select

from dscms4.orm.content.group import GroupBaseChart
from dscms4.orm.content.group import GroupConfiguration
from dscms4.orm.content.group import GroupMenu
from dscms4.orm.group import Group, GroupMemberTerminal


__all__ = ['get_groups_tree', 'GroupContent']


LOGGER = getLogger(__file__)


def get_groups_tree():
    """Returns the management tree."""

    root_groups = Group.select().where(
        (Group.customer == CUSTOMER.id) & (Group.parent >> None))

    for root_group in root_groups:
        yield GroupContent(root_group)


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
        for group_base_chart in GroupBaseChart.select().where(
                GroupBaseChart.group == self.group):
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
        if 'noasync' in request.args:
            LOGGER.warning('Retrieving content and terminals non-async.')
            content = {
                'charts': list(self.charts),
                'configurations': list(self.configurations),
                'menus': list(self.menus)}
            return (content, list(self.terminals))

        results = async_select(
            charts=self.charts, configurations=self.configurations,
            menus=self.menus, terminals=self.terminals)
        terminals = results.pop('terminals')
        return (results, terminals)

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
