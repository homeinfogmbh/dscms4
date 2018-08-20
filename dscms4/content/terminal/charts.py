"""Charts of terminals."""

from dscms4.content.common import ContentInformation, get_charts, \
    terminal_groups
from dscms4.content.group.charts import \
    accumulated_base_charts as _accumulated_base_charts, \
    accumulated_charts as _accumulated_charts
from dscms4.orm.content.terminal import TerminalBaseChart


__all__ = ['base_charts', 'accumulated_base_charts']


def _base_charts(terminal):
    """Yields base charts of the terminal."""

    for terminal_base_chart in TerminalBaseChart.select().where(
            TerminalBaseChart.terminal == terminal):
        yield terminal_base_chart.base_chart


def base_charts(terminal):
    """Yields base charts of the terminal."""

    for base_chart in _base_charts(terminal):
        yield ContentInformation(terminal, base_chart)


def accumulated_base_charts(terminal):
    """Yields accumulated base charts."""

    yield from base_charts(terminal)

    for group in terminal_groups(terminal):
        yield from _accumulated_base_charts(group)


def charts(terminal):
    """Yields charts of the terminal."""

    for chart in get_charts(_base_charts(terminal)):
        yield ContentInformation(terminal, chart)


def accumulated_charts(terminal):
    """Yields accumulated charts of the terminal."""

    yield from charts(terminal)

    for group in terminal_groups(terminal):
        yield from _accumulated_charts(group)
