"""Terminal related messages."""

from his.messages import locales, Message

__all__ = ['NoSuchTerminal']


class TerminalMessage(Message):
    """Base class for terminal related messages."""

    LOCALES = locales('/etc/dscms4.d/locales/terminal.ini')
    ABSTRACT = True


class NoSuchTerminal(TerminalMessage):
    """Indicates that the respective terminal does not exist."""

    STATUS = 404
