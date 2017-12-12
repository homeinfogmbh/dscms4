"""Management of tickers in terminals."""

from peewee import DoesNotExist

from wsgilib import JSON

from dscms4.messages.content.terminal import NoSuchTerminalTicker, \
    TickerAddedToTerminal, TickerAlreadyInTerminal, TickerDeletedFromTerminal
from dscms4.orm.content.terminal import TerminalTicker
from dscms4.wsgi.terminal import _get_terminal
from dscms4.wsgi.ticker import _get_ticker

__all__ = ['get_terminal_tickers', 'add_terminal_ticker']


def get_terminal_tickers(gid):
    """Returns a list of IDs of the menus in the respective terminal."""

    return JSON([
        terminal_ticker.ticker.id for terminal_ticker
        in TerminalTicker.select().where(
            TerminalTicker.terminal == _get_terminal(gid))])


def add_terminal_ticker(gid, ident):
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


def delete_terminal_menu(gid, ident):
    """Deletes the menu from the respective terminal."""

    try:
        terminal_ticker = TerminalTicker.get(
            (TerminalTicker.terminal == _get_terminal(gid))
            & (TerminalTicker.id == ident))
    except DoesNotExist:
        raise NoSuchTerminalTicker()

    terminal_ticker.delete_instance()
    return TickerDeletedFromTerminal()
