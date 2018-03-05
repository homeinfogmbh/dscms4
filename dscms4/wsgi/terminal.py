"""Terminal-related requests."""

from his import CUSTOMER, authenticated, authorized
from terminallib import Terminal
from wsgilib import JSON

from dscms4.messages.terminal import NoSuchTerminal

__all__ = ['get_terminal', 'ROUTES']


def get_terminal(tid):
    """Returns the respective terminal."""

    try:
        return Terminal.get(
            (Terminal.customer == CUSTOMER.id) & (Terminal.tid == tid))
    except Terminal.DoesNotExist:
        raise NoSuchTerminal()


@authenticated
@authorized('dscms4')
def list_():
    """Lists all terminals of the respective customer."""

    return JSON([
        terminal.to_dict(short=True) for terminal in Terminal.select().where(
            Terminal.customer == CUSTOMER.id)])


@authenticated
@authorized('dscms4')
def get(tid):
    """Returns the respective terminal."""

    return JSON(get_terminal(tid).to_dict())


ROUTES = (
    ('GET', '/terminal', list_, 'list_terminals'),
    ('GET', '/terminal/<int:tid>', get, 'get_terminal'))
