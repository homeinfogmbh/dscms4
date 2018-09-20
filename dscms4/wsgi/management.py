"""Management endpoint."""

from collections import defaultdict

from his import CUSTOMER, authenticated, authorized

from terminallib import Terminal
from wsgilib import JSON

from dscms4.orm.charts import BaseChart, Chart, ChartMode
from dscms4.orm.configuration import Configuration
from dscms4.orm.content.group import GroupBaseChart
from dscms4.orm.content.group import GroupConfiguration
from dscms4.orm.content.group import GroupMenu
from dscms4.orm.content.terminal import TerminalBaseChart
from dscms4.orm.content.terminal import TerminalConfiguration
from dscms4.orm.content.terminal import TerminalMenu
from dscms4.orm.group import Group, GroupMemberTerminal
from dscms4.orm.menu import Menu


__all__ = ['ROUTES']


class TerminalContent:
    """Represents content of a terminal."""

    def __init__(self, terminal):
        """Sets the terminal."""
        self.terminal = terminal

    @property
    def tid(self):
        """Returns the terminal TID."""
        return self.terminal.tid

    @property
    def charts(self):
        """Yields the terminal's charts."""
        for tbc in TerminalBaseChart.select().where(
                TerminalBaseChart.terminal == self.terminal):
            yield tbc.base_chart.chart

    @property
    def configurations(self):
        """Yields the terminal's configurations."""
        for terminal_config in TerminalConfiguration.select().where(
                TerminalConfiguration.terminal == self.terminal):
            yield terminal_config.configuration

    @property
    def menus(self):
        """Yields the terminal's menus."""
        for terminal_menu in TerminalMenu.select().where(
                TerminalMenu.terminal == self.terminal):
            yield terminal_menu.menu

    def to_json(self):
        """Returns the terminal and its content as a JSON-ish dict."""
        json = self.terminal.to_json()
        charts = [chart.to_json() for chart in self.charts]
        configurations = [config.to_json() for config in self.configurations]
        menus = [menu.to_json() for menu in self.menus]
        content = {
            'charts': charts,
            'configurations': configurations,
            'menus':menus}
        json['content'] = content
        return json


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
        for gbc in GroupBaseChart.select().where(
                GroupBaseChart.group == self.group):
            yield gbc.base_chart.chart

    @property
    def configurations(self):
        """Yields the group's configurations."""
        for group_config in GroupConfiguration.select().where(
                GroupConfiguration.group == self.group):
            yield group_config.configuration

    @property
    def menus(self):
        """Yields the group's menus."""
        for group_menu in GroupMenu.select().where(
                GroupMenu.group == self.group):
            yield group_menu.menu

    @property
    def terminals(self):
        """Yields the group's terminals."""
        for gmt in GroupMemberTerminal.select().where(
                GroupMemberTerminal.group == self.group):
            yield gmt.member

    def to_json(self):
        """Recursively converts the group content into a JSON-ish dict."""
        json = self.group.to_json(parent=False)
        children = [group.to_json() for group in self.children]
        json['children'] = children
        charts = [chart.to_json(mode=ChartMode.BRIEF) for chart in self.charts]
        configurations = [config.id for config in self.configurations]
        menus = [menu.id for menu in self.menus]
        content = {
            'charts': charts,
            'configurations': configurations,
            'menus':menus}
        json['content'] = content
        terminals = [terminal.tid for terminal in self.terminals]
        menbers = {'terminals': terminals}
        json['members'] = menbers
        return json


def get_groups_tree():
    """Returns the management tree."""

    root_groups = Group.select().where(
        (Group.customer == CUSTOMER.id) & (Group.parent >> None))

    for root_group in root_groups:
        yield GroupContent(root_group)


def get_terminals():
    """Yields terminals that are not in any group."""

    for terminal in Terminal.select().where(
            (Terminal.customer == CUSTOMER.id)
            & (Terminal.testing == 0)
            & (Terminal.deleted >> None)):
        yield TerminalContent(terminal)


def get_charts():
    """Yields the customer's charts."""

    for type_name, chart_type in Chart.types.items():
        for chart in chart_type.select().join(BaseChart).where(
                BaseChart.customer == CUSTOMER.id):
            yield (type_name, chart)


def get_configurations():
    """Yields the customer's configurations."""

    return Configuration.select().where(Configuration.customer == CUSTOMER.id)


def get_menus():
    """Yields the customer's menus."""

    return Menu.seletc().where(Menu.customer == CUSTOMER.id)



def get_management():
    """Returns the management data for the current customer."""

    groups = [group.to_json() for group in get_groups_tree()]
    terminals = {terminal.tid: terminal.to_json() for terminal in get_terminals()}
    charts = defaultdict(dict)

    for type_name, chart in get_charts():
        charts[type_name][chart.id] = chart.to_json()

    configurations = {
        configuration.id: configuration.to_json()
        for configuration in get_configurations()}
    menus = {menu.id: menu.to_json() for menu in get_menus()}

    return {
        'groups': groups,
        'terminals': terminals,
        'charts': charts,
        'configurations': configurations,
        'menus': menus}


@authenticated
@authorized('dscms4')
def list_():
    """Lists the management data."""

    return JSON(get_management())


ROUTES = (('GET', '/management', list_, 'get_management'),)
