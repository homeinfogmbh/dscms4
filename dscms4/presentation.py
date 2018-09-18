"""Content accumulation for terminals."""

from functools import lru_cache
from logging import getLogger

from functoolsplus import coerce    # pylint: disable=E0401

from dscms4 import dom  # pylint: disable=E0611
from dscms4.exceptions import OrphanedBaseChart, AmbiguousBaseChart
from dscms4.exceptions import NoConfigurationFound
from dscms4.orm.charts import BaseChart, ChartMode
from dscms4.orm.configuration import Configuration
from dscms4.orm.content.terminal import TerminalBaseChart
from dscms4.orm.content.terminal import TerminalConfiguration
from dscms4.orm.content.terminal import TerminalMenu
from dscms4.orm.content.group import GroupBaseChart
from dscms4.orm.content.group import GroupConfiguration
from dscms4.orm.content.group import GroupMenu
from dscms4.orm.group import GroupMemberTerminal
from dscms4.orm.menu import Menu


__all__ = ['Presentation']


LOGGER = getLogger(__file__)


class Presentation:
    """Accumulates content for a terminal."""

    def __init__(self, terminal):
        """Sets the respective terminal."""
        self.terminal = terminal

    @property
    @lru_cache()
    @coerce(set)
    def groups(self):
        """Yields groups this terminal is a member of."""
        for gmt in GroupMemberTerminal.select().where(
                GroupMemberTerminal.terminal == self.terminal):
            group = gmt.group

            while group is not None:
                yield group
                group = group.parent

    @property
    @lru_cache()
    def configuration(self):
        """Returns the terminal's configuration."""
        for configuration in Configuration.select().join(
                TerminalConfiguration).where(
                    TerminalConfiguration.terminal == self.terminal):
            return configuration

        for configuration in Configuration.select().join(
                GroupConfiguration).where(
                    GroupConfiguration.group << self.groups):
            return configuration

        raise NoConfigurationFound()

    @property
    @lru_cache()
    @coerce(tuple)
    def menus(self):
        """Yields menus of this terminal."""
        # Menus directly attached to the terminal.
        yield from Menu.select().join(TerminalMenu).where(
            TerminalMenu.terminal == self.terminal)

        # Menus attached to groups the terminal is a member of.
        yield from Menu.select().join(GroupMenu).where(
            GroupMenu.group << self.groups)

    @property
    @lru_cache()
    @coerce(tuple)
    def base_charts(self):
        """Yields the terminal's base charts."""
        # Charts directy attached to the terminal.
        yield from BaseChart.select().join(TerminalBaseChart).where(
            (BaseChart.trashed == 0)
            & (TerminalBaseChart.terminal == self.terminal))

        # Charts attached to groups, the terminal is a member of.
        yield from BaseChart.select().join(GroupBaseChart).where(
            (BaseChart.trashed == 0) &
            (GroupBaseChart.group << self.groups))

    @property
    @lru_cache()
    @coerce(tuple)
    def charts(self):
        """Yields the terminal's charts."""
        for base_chart in self.base_charts:
            try:
                yield base_chart.chart
            except OrphanedBaseChart:
                LOGGER.error('Base chart is orphaned: %s.', base_chart)
            except AmbiguousBaseChart:
                LOGGER.error('Base chart is ambiguous: %s.', base_chart)

    @property
    @lru_cache()
    @coerce(set)
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
        xml.playlist = [chart.to_dom(brief=True) for chart in self.charts]
        xml.menu = [menu.to_dom() for menu in self.menus]
        xml.chart = [chart.to_dom() for chart in self.charts]
        return xml

    def to_json(self):
        """Returns a JSON presentation."""
        return {
            'customer': self.terminal.customer.id,
            'tid': self.terminal.tid,
            'configuration': self.configuration.to_json(),
            'playlist': [
                chart.to_json(mode=ChartMode.BRIEF) for chart in self.charts],
            'menus': [menu.to_json() for menu in self.menus],
            'charts': [chart.to_json() for chart in self.charts]}
