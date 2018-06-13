"""Terminal related messages."""

from his.messages import Message

__all__ = ['NoSuchTerminal']


class TerminalMessage(Message):
    """Base class for terminal related messages."""

    LOCALES = '/etc/dscms4.d/locales/terminal.ini'


class NoSuchTerminal(TerminalMessage):
    """Indicates that the respective terminal does not exist."""

    STATUS = 404
