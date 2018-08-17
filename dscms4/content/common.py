"""Content information."""

from collections import namedtuple
from logging import getLogger

from dscms4.exceptions import OrphanedBaseChart, AmbiguousBaseChart
from dscms4.orm.group import GroupMemberTerminal
from dscms4.orm.util import chart_of

__all__ = ['ContentInformation', 'get_charts', 'terminal_groups']


LOGGER = getLogger(__file__)
ContentInformation = namedtuple('ContentInformation', ('owner', 'content'))


def get_charts(base_charts):
    """Yields the corresponding charts."""

    for base_chart in base_charts:
        try:
            yield chart_of(base_chart)
        except OrphanedBaseChart:
            LOGGER.error('Base chart is orphaned: %s.', base_chart)
        except AmbiguousBaseChart:
            LOGGER.error('Base chart is ambiguous: %s.', base_chart)


def terminal_groups(terminal):
    """Yields the groups the terminal is member of."""

    for group_member_terminal in GroupMemberTerminal.select().where(
            GroupMemberTerminal.terminal == terminal):
        yield group_member_terminal.group
