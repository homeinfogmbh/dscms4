"""Management of tickers in terminals."""

from peewee import DoesNotExist

from wsgilib import JSON

from dscms4.messages.content.terminal import NoSuchTerminalTicker, \
    TickerAddedToTerminal, TickerAlreadyInTerminal, TickerDeletedFromTerminal
from dscms4.orm.content.terminal import TerminalTicker
from dscms4.wsgi.terminal import _get_terminal
from dscms4.wsgi.ticker import _get_ticker

__all__ = ['ROUTES']


def get(gid):
    """Returns a list of IDs of the menus in the respective terminal."""

    return JSON([
        terminal_ticker.ticker.id for terminal_ticker
        in TerminalTicker.select().where(
            TerminalTicker.terminal == _get_terminal(gid))])


def add(gid, ident):
    """Adds the menu to the respective terminal."""

    terminal = _get_terminal(gid)
    ticker = _get_ticker(ident)

    try:
        TerminalTicker.get(
            (TerminalTicker.terminal == terminal)
            & (TerminalTicker.ticker == ticker))
    except DoesNotExist:
        terminal_ticker = TerminalTicker()
        terminal_ticker.terminal = terminal
        terminal_ticker.ticker = ticker
        terminal_ticker.save()
        return TickerAddedToTerminal()

    return TickerAlreadyInTerminal()


def delete(gid, ident):
    """Deletes the menu from the respective terminal."""

    try:
        terminal_ticker = TerminalTicker.get(
            (TerminalTicker.terminal == _get_terminal(gid))
            & (TerminalTicker.id == ident))
    except DoesNotExist:
        raise NoSuchTerminalTicker()

    terminal_ticker.delete_instance()
    return TickerDeletedFromTerminal()


ROUTES = (
    ('GET', '/content/terminal/<int:gid>/ticker', get,
     'list_terminal_tickers'),
    ('POST', '/content/terminal/<int:gid>/ticker', add, 'add_terminal_ticker'),
    ('DELETE', '/content/terminal/<int:gid>/ticker/<int:ident>', delete,
     'delete_terminal_ticker'))
