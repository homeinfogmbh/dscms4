"""Management of tickers in terminals."""

from his import authenticated, authorized
from wsgilib import JSON

from dscms4.messages.content import NoSuchContent, ContentAdded, \
    ContentExists, ContentDeleted
from dscms4.orm.content.terminal import TerminalTicker
from dscms4.wsgi.terminal import get_terminal
from dscms4.wsgi.ticker import get_ticker

__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(gid):
    """Returns a list of IDs of the menus in the respective terminal."""

    return JSON([
        terminal_ticker.ticker.id for terminal_ticker
        in TerminalTicker.select().where(
            TerminalTicker.terminal == get_terminal(gid))])


@authenticated
@authorized('dscms4')
def add(gid, ident):
    """Adds the menu to the respective terminal."""

    terminal = get_terminal(gid)
    ticker = get_ticker(ident)

    try:
        TerminalTicker.get(
            (TerminalTicker.terminal == terminal)
            & (TerminalTicker.ticker == ticker))
    except TerminalTicker.DoesNotExist:
        terminal_ticker = TerminalTicker()
        terminal_ticker.terminal = terminal
        terminal_ticker.ticker = ticker
        terminal_ticker.save()
        return ContentAdded()

    return ContentExists()


@authenticated
@authorized('dscms4')
def delete(gid, ident):
    """Deletes the menu from the respective terminal."""

    try:
        terminal_ticker = TerminalTicker.get(
            (TerminalTicker.terminal == get_terminal(gid))
            & (TerminalTicker.id == ident))
    except TerminalTicker.DoesNotExist:
        raise NoSuchContent()

    terminal_ticker.delete_instance()
    return ContentDeleted()


ROUTES = (
    ('GET', '/content/terminal/<int:gid>/ticker', get,
     'list_terminal_tickers'),
    ('POST', '/content/terminal/<int:gid>/ticker/<int:ident>', add,
     'add_terminal_ticker'),
    ('DELETE', '/content/terminal/<int:gid>/ticker/<int:ident>', delete,
     'delete_terminal_ticker'))
