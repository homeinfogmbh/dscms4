"""Groups tree endpoint."""

from asyncio import coroutine, get_event_loop, sleep, wait

from his import CUSTOMER, authenticated, authorized

from wsgilib import JSON

from dscms4.orm.content.group import GroupBaseChart
from dscms4.orm.content.group import GroupConfiguration
from dscms4.orm.content.group import GroupMenu
from dscms4.orm.group import Group, GroupMemberTerminal
from dscms4.wsgi.group.group import get_group


__all__ = ['ROUTES']


def get_groups_tree():
    """Returns the management tree."""

    root_groups = Group.select().where(
        (Group.customer == CUSTOMER.id) & (Group.parent >> None))

    for root_group in root_groups:
        yield GroupContent(root_group)


@coroutine
def async_list(name, generator):
    """Async list generator."""

    result = []

    for item in generator:
        result.append(item.to_json())
        yield from sleep(0)

    return (name, result)


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
        return GroupBaseChart.select().where(
            GroupBaseChart.group == self.group)

    @property
    def configurations(self):
        """Yields the group's configurations."""
        return GroupConfiguration.select().where(
            GroupConfiguration.group == self.group)

    @property
    def menus(self):
        """Yields the group's menus."""
        return GroupMenu.select().where(GroupMenu.group == self.group)

    @property
    def terminals(self):
        """Yields the group's terminals."""
        return GroupMemberTerminal.select().where(
            GroupMemberTerminal.group == self.group)

    @coroutine
    def async_content(self):
        """Generates async content."""
        charts = async_list('charts', self.charts)
        configurations = async_list('configurations', self.configurations)
        menus = async_list('menus', self.menus)
        terminals = async_list('terminals', self.terminals)
        return wait((charts, configurations, menus, terminals))

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
        # Async content.
        loop = get_event_loop()
        tasks, _ = loop.run_until_complete(self.async_content())
        json = {key: value for key, value in (task.result() for task in tasks)}
        print('JSON:', json, flush=True)
        menbers = {'terminals': json.pop('terminals')}
        json['members'] = menbers
        json['content'] = json
        return json


ROUTES = (
    ('GET', '/grouptree', groups_tree, 'groups_tree'),
    ('GET', '/grouptree/<int:gid>', groups_subtree, 'groups_subtree'))
