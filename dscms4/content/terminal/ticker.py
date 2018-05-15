"""Terminal tickers."""

from dscms4.content.common import ContentInformation, terminal_groups
from dscms4.content.group.ticker import \
    accumulated_tickers as _accumulated_tickers
from dscms4.orm.content.terminal import TerminalTicker

__all__ = ['tickers', 'accumulated_tickers']


def tickers(terminal):
    """Yields the tickers of the terminal."""

    for terminal_ticker in TerminalTicker.select().where(
            TerminalTicker.terminal == terminal):
        yield ContentInformation(terminal, terminal_ticker.ticker)


def accumulated_tickers(terminal):
    """Yields accumulated tickers of the terminal."""

    yield from tickers(terminal)

    for group in terminal_groups(terminal):
        yield from _accumulated_tickers(group)
