"""Management of charts in terminals."""

from his import authenticated, authorized
from wsgilib import JSON

from dscms4.messages.content import NoSuchContent, ContentAdded, \
    ContentExists, ContentDeleted
from dscms4.orm.content.terminal import TerminalBaseChart
from dscms4.orm.util import chart_of
from dscms4.wsgi.charts import get_chart
from dscms4.wsgi.terminal import get_terminal

__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(tid):
    """Returns a list of IDs of the charts in the respective terminal."""

    return JSON([
        chart_of(tbc.base_chart).to_dict()
        for tbc in TerminalBaseChart.select().where(
            TerminalBaseChart.terminal == get_terminal(tid))])


@authenticated
@authorized('dscms4')
def add(tid, ident):
    """Adds the chart to the respective terminal."""

    terminal = get_terminal(tid)
    base_chart = get_chart(ident).base

    try:
        TerminalBaseChart.get(
            (TerminalBaseChart.terminal == terminal)
            & (TerminalBaseChart.base_chart == base_chart))
    except TerminalBaseChart.DoesNotExist:
        tbc = TerminalBaseChart()
        tbc.terminal = terminal
        tbc.base_chart = base_chart
        tbc.save()
        return ContentAdded()

    return ContentExists()


@authenticated
@authorized('dscms4')
def delete(tid, ident):
    """Deletes the chart from the respective terminal."""

    terminal = get_terminal(tid)
    base_chart = get_chart(ident).base

    try:
        terminal_chart = TerminalBaseChart.get(
            (TerminalBaseChart.terminal == terminal)
            & (TerminalBaseChart.base_chart == base_chart))
    except TerminalBaseChart.DoesNotExist:
        raise NoSuchContent()

    terminal_chart.delete_instance()
    return ContentDeleted()


ROUTES = (
    ('GET', '/content/terminal/<int:tid>/chart', get, 'list_terminal_charts'),
    ('POST', '/content/terminal/<int:tid>/chart/<int:ident>', add,
     'add_terminal_chart'),
    ('DELETE', '/content/terminal/<int:tid>/chart/<int:ident>', delete,
     'delete_terminal_chart'))
