"""Management of charts in terminals."""

from his import authenticated, authorized
from wsgilib import JSON

from dscms4.messages.content import NoSuchContent, ContentAdded, \
    ContentExists, ContentDeleted
from dscms4.orm.content.terminal import TerminalBaseChart
from dscms4.wsgi.charts import get_chart
from dscms4.wsgi.terminal import get_terminal

__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(tid):
    """Returns a list of IDs of the charts in the respective terminal."""

    return JSON([
        tbc.chart.id for tbc in TerminalBaseChart.select().where(
            TerminalBaseChart.terminal == get_terminal(tid))])


@authenticated
@authorized('dscms4')
def add(tid, ident):
    """Adds the chart to the respective terminal."""

    terminal = get_terminal(tid)
    chart = get_chart(ident)

    try:
        TerminalBaseChart.get(
            (TerminalBaseChart.terminal == terminal)
            & (TerminalBaseChart.chart == chart))
    except TerminalBaseChart.DoesNotExist:
        tbc = TerminalBaseChart()
        tbc.terminal = terminal
        tbc.chart = chart
        tbc.save()
        return ContentAdded()

    return ContentExists()


@authenticated
@authorized('dscms4')
def delete(tid, ident):
    """Deletes the chart from the respective terminal."""

    terminal = get_terminal(tid)
    chart = get_chart(ident)

    try:
        terminal_chart = TerminalBaseChart.get(
            (TerminalBaseChart.terminal == terminal)
            & (TerminalBaseChart.chart == chart))
    except TerminalBaseChart.DoesNotExist:
        raise NoSuchContent()

    terminal_chart.delete_instance()
    return ContentDeleted()


ROUTES = (
    ('GET', '/content/terminal/<int:gid>/chart', get, 'list_terminal_charts'),
    ('POST', '/content/terminal/<int:gid>/chart/<int:ident>', add,
     'add_terminal_chart'),
    ('DELETE', '/content/terminal/<int:gid>/chart/<int:ident>', delete,
     'delete_terminal_chart'))
