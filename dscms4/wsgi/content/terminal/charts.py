"""Management of charts in terminals."""

from peewee import DoesNotExist

from wsgilib import JSON

from dscms4.messages.content.terminal import NoSuchTerminalChart, \
    ChartAddedToTerminal, ChartAlreadyInTerminal, ChartDeletedFromTerminal
from dscms4.messages.terminal import NoSuchTerminal
from dscms4.orm.content.terminal import TerminalBaseChart
from dscms4.wsgi.chart import _get_chart
from dscms4.wsgi.terminal import _get_terminal

__all__ = [
    'get_terminal_charts',
    'add_terminal_chart',
    'delete_terminal_chart']


def get_terminal_charts(tid):
    """Returns a list of IDs of the charts in the respective terminal."""

    return JSON([tbc.chart.id for tbc in TerminalBaseChart.select().where(
        TerminalBaseChart.terminal == _get_terminal(tid))])


def add_terminal_chart(tid, ident):
    """Adds the chart to the respective terminal."""

    terminal = _get_terminal(tid)
    chart = _get_chart(ident)

    try:
        TerminalBaseChart.get(
            (TerminalBaseChart.terminal == terminal)
            & (TerminalBaseChart.chart == chart))
    except DoesNotExist:
        tbc = TerminalBaseChart()
        tbc.terminal = terminal
        tbc.chart = chart
        tbc.save()
        return ChartAddedToTerminal()

    return ChartAlreadyInTerminal()


def delete_terminal_chart(tid, ident):
    """Deletes the chart from the respective terminal."""

    try:
        terminal_chart = TerminalBaseChart.get(
            (TerminalBaseChart.terminal == _get_terminal(tid))
            & (TerminalBaseChart.id == ident))
    except DoesNotExist:
        raise NoSuchTerminalChart()

    terminal_chart.delete_instance()
    return ChartDeletedFromTerminal()
