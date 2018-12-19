"""Content accumulation for terminals."""

from itertools import chain

from functoolsplus import cached_method, coerce    # pylint: disable=E0401

from dscms4.exceptions import AmbiguousConfigurationsError
from dscms4.exceptions import NoConfigurationFound
from dscms4.orm.charts import BaseChart
from dscms4.orm.configuration import Configuration
from dscms4.orm.content.terminal import TerminalBaseChart
from dscms4.orm.content.terminal import TerminalConfiguration
from dscms4.orm.content.terminal import TerminalMenu
from dscms4.orm.content.group import GroupBaseChart
from dscms4.orm.content.group import GroupMenu
from dscms4.orm.group import GroupMemberTerminal
from dscms4.orm.menu import Menu

from dscms4.presentation.common import charts
from dscms4.presentation.common import indexify
from dscms4.presentation.common import level_configs
from dscms4.presentation.common import PresentationMixin


__all__ = ['Presentation']


class Presentation(PresentationMixin):
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

        for base_chart_mapping in sorted(chain(tbcs, gbcs), key=indexify):
            yield base_chart_mapping.base_chart
