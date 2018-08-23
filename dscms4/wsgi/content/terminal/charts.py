"""Management of charts in terminals."""

from his import CUSTOMER, authenticated, authorized
from terminallib import Terminal
from wsgilib import JSON

from dscms4.messages.content import NoSuchContent, ContentAdded, \
    ContentDeleted
from dscms4.orm.content.terminal import TerminalBaseChart
from dscms4.wsgi.charts import get_chart
from dscms4.wsgi.terminal import get_terminal

__all__ = ['ROUTES']


def _select_tbc(tid):
    """Returns the respective terminal base chart."""

    return TerminalBaseChart.select().join(Terminal).where(
        (Terminal.customer == CUSTOMER.id) & (Terminal.tid == tid))


def _get_tbc(tid, ident):
    """Returns the respective terminal base chart."""

    try:
        return TerminalBaseChart.select().join(Terminal).where(
            (TerminalBaseChart.id == ident)
            & (Terminal.customer == CUSTOMER.id)
            & (Terminal.tid == tid)).get()
    except TerminalBaseChart.DoesNotExist:
        raise NoSuchContent()


@authenticated
@authorized('dscms4')
def get(tid):
    """Returns a list of IDs of the charts in the respective terminal."""

    return JSON([tbc.to_json() for tbc in _select_tbc(tid)])


@authenticated
@authorized('dscms4')
def add(tid, ident):
    """Adds the chart to the respective terminal."""

    terminal = get_terminal(tid)
    base_chart = get_chart(ident).base
    tbc = TerminalBaseChart()
    tbc.terminal = terminal
    tbc.base_chart = base_chart
    tbc.save()
    return ContentAdded(id=tbc.id)


@authenticated
@authorized('dscms4')
def delete(tid, ident):
    """Deletes the chart from the respective terminal."""

    _get_tbc(tid, ident).delete_instance()
    return ContentDeleted()


ROUTES = (
    ('GET', '/content/terminal/<int:tid>/chart', get, 'list_terminal_charts'),
    ('POST', '/content/terminal/<int:tid>/chart/<int:ident>', add,
     'add_terminal_chart'),
    ('DELETE', '/content/terminal/<int:tid>/chart/<int:ident>', delete,
     'delete_terminal_chart'))
