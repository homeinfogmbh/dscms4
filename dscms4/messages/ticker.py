"""Ticker related messages."""

from his.messages import locales, Message

__all__ = ['NoSuchTicker', 'TickerAdded', 'TickerPatched', 'TickerDeleted']


class TickerMessage(Message):
    """Base class for ticker related messages."""

    LOCALES = locales('/etc/dscms4.d/locales/ticker.ini')
    ABSTRACT = True


class NoSuchTicker(TerminalMessage):
    """Indicates that the respective ticker does not exist."""

    STATUS = 404


class TickerAdded(TerminalMessage):
    """Indicates that the respective ticker was successfully added."""

    STATUS = 201


class TickerPatched(TerminalMessage):
    """Indicates that the respective ticker was successfully patched."""

    STATUS = 200


class TickerDeleted(TerminalMessage):
    """Indicates that the respective ticker was successfully deleted."""

    STATUS = 200
