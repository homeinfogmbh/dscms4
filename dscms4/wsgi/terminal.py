"""Terminal-related requests."""

from flask import request

from his import CUSTOMER, authenticated, authorized
from his.messages import MissingData, InvalidData
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


def _page():
    """Returns the respective terminal page."""

    try:
        size = int(request.args['size'])
    except KeyError:
        raise MissingData(parameter='size')
    except ValueError:
        raise InvalidData(parameter='size')

    try:
        page_number = int(request.args['page'])
    except KeyError:
        raise MissingData(parameter='page')
    except ValueError:
        raise InvalidData(parameter='page')

    offset = size * page_number
    end = offset + size

    for index, terminal in enumerate(Terminal.select().where(
            Terminal.customer == CUSTOMER.id)):
        if offset <= index < end:
            yield terminal


@authenticated
@authorized('dscms4')
def list_():
    """Lists all terminals of the respective customer."""

    if 'page' in request.args or 'size' in request.args:
        return JSON([terminal.to_dict(short=True) for terminal in _page()])


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
