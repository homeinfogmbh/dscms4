"""Terminal-related requests."""

from peewee import DoesNotExist

from his import CUSTOMER
from terminallib import Terminal
from wsgilib import JSON

from dscms4.messages.terminal import NoSuchTerminal

__all__ = ['ROUTES']


def _get_terminal(tid):
    """Returns the respective terminal."""

    try:
        return Terminal.get(
            (Terminal.customer == CUSTOMER.id) & (Terminal.tid == tid))
    except DoesNotExist:
        raise NoSuchTerminal()


@authenticated
@authorized('dscms4')
def lst():
    """Lists all terminals of the respective customer."""

    return JSON([terminal.to_dict() for terminal in Terminal.select().where(
        Terminal.customer == CUSTOMER.id)])


@authenticated
@authorized('dscms4')
def get(tid):
    """Returns the respective terminal."""

    return JSON(_get_terminal(tid).to_dict())


ROUTES = (
    ('GET', '/terminal', lst, 'list_terminals'),
    ('GET', '/terminal/<int:tid>', get, 'get_terminal'))
