"""Ticker related messages."""

from his.messages import locales, Message

__all__ = [
    'NoSuchTicker',
    'TickerAdded',
    'TickerPatched',
    'TickerDeleted',
    'NoSuchTickerText',
    'TickerTextAdded',
    'TickerTextPatched',
    'TickerTextDeleted',
    'NoSuchTickerURL',
    'TickerURLAdded',
    'TickerURLPatched',
    'TickerURLDeleted']


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


class NoSuchTickerText(TerminalMessage):
    """Indicates that the respective ticker text does not exist."""

    STATUS = 404


class TickerTextAdded(TerminalMessage):
    """Indicates that the respective ticker text was successfully added."""

    STATUS = 201


class TickerTextPatched(TerminalMessage):
    """Indicates that the respective ticker text was successfully patched."""

    STATUS = 200


class TickerTextDeleted(TerminalMessage):
    """Indicates that the respective ticker URL was successfully deleted."""

    STATUS = 200


class NoSuchTickerURL(TerminalMessage):
    """Indicates that the respective ticker URL does not exist."""

    STATUS = 404


class TickerURLAdded(TerminalMessage):
    """Indicates that the respective ticker URL was successfully added."""

    STATUS = 201


class TickerURLPatched(TerminalMessage):
    """Indicates that the respective ticker URL was successfully patched."""

    STATUS = 200


class TickerURLDeleted(TerminalMessage):
    """Indicates that the respective ticker text was successfully deleted."""

    STATUS = 200
