"""Terminal controller."""

from peewee import DoesNotExist

from his import CUSTOMER
from terminallib import Terminal

from dscms4.messages.terminal import NoSuchTerminal

__all__ = ['list', 'get']


def _get_terminal(tid):
    """Returns the respective terminal."""

    try:
        return Terminal.get(
            (Terminal.customer == CUSTOMER.id) & (Terminal.tid == tid))
    except DoesNotExist:
        raise NoSuchTerminal()


def list():
    """Lists all terminals of the respective customer."""

    return JSON([terminal.to_dict() for terminal in Terminal.select().where(
        Terminal.customer == CUSTOMER.id)])


def get(tid):
    """Returns the respective terminal."""

    return JSON(_get_terminal(tid).to_dict())
