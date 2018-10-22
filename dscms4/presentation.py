"""Content accumulation for terminals."""

from itertools import chain
from logging import getLogger

from functoolsplus import cached_method, coerce    # pylint: disable=E0401

from dscms4 import dom  # pylint: disable=E0611
from dscms4.exceptions import AmbiguousBaseChart
from dscms4.exceptions import AmbiguousConfigurationsError
from dscms4.exceptions import NoConfigurationFound
from dscms4.exceptions import OrphanedBaseChart
from dscms4.orm.charts import BaseChart, ChartMode
from dscms4.orm.configuration import Configuration
from dscms4.orm.content.terminal import TerminalBaseChart
from dscms4.orm.content.terminal import TerminalConfiguration
from dscms4.orm.content.terminal import TerminalMenu
from dscms4.orm.content.group import GroupBaseChart
from dscms4.orm.content.group import GroupConfiguration
from dscms4.orm.content.group import GroupMenu
from dscms4.orm.group import GroupMemberTerminal
from dscms4.orm.menu import Menu, MenuItem, MenuItemChart


__all__ = ['Presentation']


LOGGER = getLogger(__file__)


@coerce(frozenset)
def charts(base_charts):
    """Yields the charts of the respective base charts."""

    for base_chart in base_charts:
        try:
            yield base_chart.chart
        except OrphanedBaseChart:
            LOGGER.error('Base chart is orphaned: %s.', base_chart)
        except AmbiguousBaseChart:
            LOGGER.error('Base chart is ambiguous: %s.', base_chart)


@coerce(frozenset)
def level_configs(level):
    """Yields all configurations of a certain group level."""

    return Configuration.select().join(GroupConfiguration).where(
        GroupConfiguration.group << level)


class Presentation:
    """Accumulates content for a terminal."""

    def __init__(self, terminal):
        """Sets the respective terminal."""
        self.terminal = terminal
        self.cache = {}

    @property
    def _direct_groups(self):
        """Yields groups this terminal is a member of."""
        for gmt in GroupMemberTerminal.select().where(
                GroupMemberTerminal.terminal == self.terminal):
            yield gmt.group

    @property
    def customer(self):
        """Returns the respective customer."""
        return self.terminal.customer

    @property
    def grouplevels(self):
        """Yields group levels in a breadth-first search."""
        level = frozenset(self._direct_groups)

        while level:
            yield level
            level = frozenset(group.parent for group in level if group.parent)

    @property
    @cached_method()
    @coerce(frozenset)
    def groups(self):
        """Yields all groups in a breadth-first search."""
        for level in self.grouplevels:
            for group in level:
                yield group

    @property
    def groupconfigs(self):
        """Returns a configuration for the terminal's groups."""
        for index, level in enumerate(self.grouplevels):
            try:
                configuration, *superfluous = level_configs(level)
            except ValueError:
                continue

            if superfluous:
                raise AmbiguousConfigurationsError(level, index)

            yield configuration

        raise NoConfigurationFound()

    @property
    def configuration(self):
        """Returns the terminal's configuration."""
        for configuration in Configuration.select().join(
                TerminalConfiguration).where(
                    TerminalConfiguration.terminal == self.terminal):
            return configuration

        for configuration in self.groupconfigs:
            return configuration

        raise NoConfigurationFound()

    @property
    @cached_method()
    @coerce(frozenset)
    def menus(self):
        """Yields menus of this terminal."""
        # Menus directly attached to the terminal.
        yield from Menu.select().join(TerminalMenu).where(
            TerminalMenu.terminal == self.terminal)

        # Menus attached to groups the terminal is a member of.
        yield from Menu.select().join(GroupMenu).where(
            GroupMenu.group << self.groups)

    @property
    @cached_method()
    @coerce(charts)
    def playlist(self):
        """Yields the terminal's base charts."""
        # Charts directy attached to the terminal.
        tbcs = TerminalBaseChart.select().join(BaseChart).where(
            (TerminalBaseChart.terminal == self.terminal)
            & (BaseChart.trashed == 0)).order_by(TerminalBaseChart.index)

        # Charts attached to groups, the terminal is a member of.
        gbcs = GroupBaseChart.select().join(BaseChart).where(
            (GroupBaseChart.group << self.groups)
            & (BaseChart.trashed == 0)).order_by(GroupBaseChart.index)

        for base_chart_mapping in sorted(
                chain(tbcs, gbcs), key=lambda record: record.index):
            yield base_chart_mapping.base_chart

    @property
    @cached_method()
    @coerce(charts)
    def menu_charts(self):
        """Yields charts of the terminal's menu."""
        yield from BaseChart.select().join(MenuItemChart).join(MenuItem).where(
            (BaseChart.trashed == 0) & (MenuItem.menu << self.menus))

    @property
    def charts(self):
        """Yields all charts for this terminal."""
        yield from self.playlist
        yield from self.menu_charts

    @property
    @cached_method()
    @coerce(frozenset)
    def files(self):
        """Yields the presentation's used file IDs."""
        yield from self.configuration.files

        for chart in self.charts:
            try:
                files = chart.files
            except AttributeError:
                continue

            yield from files

    def to_dom(self):
        """Returns an XML dom presentation."""
        xml = dom.presentation()
        xml.customer = self.terminal.customer.id
        xml.tid = self.terminal.tid
        xml.configuration = self.configuration.to_dom()
        xml.playlist = [chart.to_dom(brief=True) for chart in self.playlist]
        xml.menu = [menu.to_dom() for menu in self.menus]
        xml.chart = [chart.to_dom() for chart in self.charts]
        return xml

    def to_json(self):
        """Returns a JSON presentation."""
        return {
            'customer': self.terminal.customer.id,
            'tid': self.terminal.tid,
            'configuration': self.configuration.to_json(cascade=True),
            'playlist': [
                chart.to_json(mode=ChartMode.BRIEF)
                for chart in self.playlist],
            'menus': [menu.to_json() for menu in self.menus],
            'charts': [chart.to_json() for chart in self.charts]}
