"""Terminal controller."""

from peewee import DoesNotExist

from his import CUSTOMER
from terminallib import Terminal

from dscms4.messages.terminal import NoSuchTerminal

__all__ = ['_get_terminal']


def _get_terminal(tid):
    """Returns the respective terminal."""

    try:
        return Terminal.get(
            (Terminal.customer == CUSTOMER.id) & (Terminal.tid == tid))
    except DoesNotExist:
        raise NoSuchTerminal()
