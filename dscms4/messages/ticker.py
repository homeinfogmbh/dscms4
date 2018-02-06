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


class NoSuchTicker(TickerMessage):
    """Indicates that the respective ticker does not exist."""

    STATUS = 404


class TickerAdded(TickerMessage):
    """Indicates that the respective ticker was successfully added."""

    STATUS = 201


class TickerPatched(TickerMessage):
    """Indicates that the respective ticker was successfully patched."""

    STATUS = 200


class TickerDeleted(TickerMessage):
    """Indicates that the respective ticker was successfully deleted."""

    STATUS = 200


class NoSuchTickerText(TickerMessage):
    """Indicates that the respective ticker text does not exist."""

    STATUS = 404


class TickerTextAdded(TickerMessage):
    """Indicates that the respective ticker text was successfully added."""

    STATUS = 201


class TickerTextPatched(TickerMessage):
    """Indicates that the respective ticker text was successfully patched."""

    STATUS = 200


class TickerTextDeleted(TickerMessage):
    """Indicates that the respective ticker URL was successfully deleted."""

    STATUS = 200


class NoSuchTickerURL(TickerMessage):
    """Indicates that the respective ticker URL does not exist."""

    STATUS = 404


class TickerURLAdded(TickerMessage):
    """Indicates that the respective ticker URL was successfully added."""

    STATUS = 201


class TickerURLPatched(TickerMessage):
    """Indicates that the respective ticker URL was successfully patched."""

    STATUS = 200


class TickerURLDeleted(TickerMessage):
    """Indicates that the respective ticker text was successfully deleted."""

    STATUS = 200
