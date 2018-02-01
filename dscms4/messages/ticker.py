"""Ticker related messages."""

from his.messages import locales, Message

__all__ = ['NoSuchTicker']


class TickerMessage(Message):
    """Base class for ticker related messages."""

    LOCALES = locales('/etc/dscms4.d/locales/ticker.ini')
    ABSTRACT = True


class NoSuchTicker(TerminalMessage):
    """Indicates that the respective ticker does not exist."""

    STATUS = 404
