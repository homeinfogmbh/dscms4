"""Management of charts in terminals."""

from his import CUSTOMER, JSON_DATA, authenticated, authorized
from terminallib import Terminal
from wsgilib import JSON

from dscms4.messages.content import ContentAdded
from dscms4.messages.content import ContentDeleted
from dscms4.messages.content import ContentPatched
from dscms4.messages.content import NoSuchContent
from dscms4.orm.charts import BaseChart
from dscms4.orm.content.terminal import TerminalBaseChart
from dscms4.wsgi.charts import get_chart
from dscms4.wsgi.terminal import get_terminal

__all__ = ['ROUTES']


def list_tbc(tid):
    """Yields the terminal base charts of the
    current customer for the respective termianl.
    """

    term_join = TerminalBaseChart.terminal == Terminal.id
    bc_join = TerminalBaseChart.base_chart == BaseChart.id
    return TerminalBaseChart.select().join(
        Terminal, join_type='LEFT', on=term_join).join(
            BaseChart, join_type='LEFT', on=bc_join).where(
                (Terminal.customer == CUSTOMER.id) & (Terminal.tid == tid)
                & (BaseChart.trashed == 0))


def get_tbc(tid, ident):
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

    return JSON([tbc.to_json() for tbc in list_tbc(tid)])


@authenticated
@authorized('dscms4')
def add(tid, ident):
    """Adds the chart to the respective terminal."""

    terminal = get_terminal(tid)
    base_chart = get_chart(ident).base
    tbc = TerminalBaseChart.from_json(JSON_DATA, terminal, base_chart)
    tbc.save()
    return ContentAdded(id=tbc.id)


@authenticated
@authorized('dscms4')
def patch(tid, ident):
    """Adds the chart to the respective terminal."""

    tbc = get_tbc(tid, ident)
    tbc.patch_json(JSON_DATA)
    tbc.save()
    return ContentPatched()


@authenticated
@authorized('dscms4')
def delete(tid, ident):
    """Deletes the chart from the respective terminal."""

    terminal_base_chart = get_tbc(tid, ident)
    terminal_base_chart.delete_instance()
    return ContentDeleted()


ROUTES = (
    ('GET', '/content/terminal/<int:tid>/chart', get, 'list_terminal_charts'),
    ('POST', '/content/terminal/<int:tid>/chart/<int:ident>', add,
     'add_terminal_chart'),
    ('PATCH', '/content/terminal/<int:tid>/chart/<int:ident>', patch,
     'patch_terminal_chart'),
    ('DELETE', '/content/terminal/<int:tid>/chart/<int:ident>', delete,
     'delete_terminal_chart'))
