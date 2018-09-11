"""Terminal-related requests."""

from flask import request

from his import CUSTOMER, authenticated, authorized
from his.messages import InvalidData
from terminallib import Terminal
from wsgilib import JSON, XML

from dscms4.content.terminal.presentation import Presentation
from dscms4.content.exceptions import NoConfigurationFound
from dscms4.messages.content import NoConfigurationAssigned
from dscms4.messages.terminal import NoSuchTerminal
from dscms4.orm.util import terminal_groups
from dscms4.paging import page, pages


__all__ = ['get_terminal', 'ROUTES']


def get_terminal(tid):
    """Returns the respective terminal."""

    try:
        return Terminal.get(
            (Terminal.tid == tid) & (Terminal.customer == CUSTOMER.id))
    except Terminal.DoesNotExist:
        raise NoSuchTerminal()


def with_terminal(function):
    """Converts a TID into a terminal."""

    def wrapper(tid, *args, **kwargs):
        """Wraps the function."""
        return function(get_terminal(tid), *args, **kwargs)

    return wrapper


@authenticated
@authorized('dscms4')
def list_():
    """Lists all terminals of the respective customer."""

    expression = Terminal.customer == CUSTOMER.id

    if 'testing' not in request.args:
        expression &= Terminal.testing == 0

    terminals = Terminal.select().where(expression)

    try:
        size = int(request.args['size'])
    except KeyError:
        size = None
    except ValueError:
        raise InvalidData(parameter='size')

    try:
        pageno = int(request.args['page'])
    except KeyError:
        pageno = None
    except ValueError:
        raise InvalidData(parameter='page')

    if size is not None:
        if pageno is not None:
            return JSON([terminal.to_json(short=True) for terminal in page(
                terminals, size, pageno)])

        return JSON({'pages': pages(terminals, size)})

    return JSON([terminal.to_json(short=True) for terminal in terminals])


@authenticated
@authorized('dscms4')
@with_terminal
def get(terminal):
    """Returns the respective terminal."""

    return JSON(terminal.to_json())


@authenticated
@authorized('dscms4')
def get_groups(tid):
    """Returns the groups this terminal is a member of."""

    return JSON(terminal_groups(tid))


@authenticated
@authorized('dscms4')
@with_terminal
def get_presentation(terminal):
    """Returns the presentation for the respective terminal."""

    presentation = Presentation(terminal)

    try:
        request.args['xml']
    except KeyError:
        return JSON(presentation.to_json())

    try:
        presentation_dom = presentation.to_dom()
    except NoConfigurationFound:
        return NoConfigurationAssigned()

    return XML(presentation_dom)


ROUTES = (
    ('GET', '/terminal', list_, 'list_terminals'),
    ('GET', '/terminal/<int:tid>', get, 'get_terminal'),
    ('GET', '/terminal/<int:tid>/groups', get_groups, 'get_terminal_groups'),
    ('GET', '/terminal/<int:tid>/presentation', get_presentation,
     'get_terminal_presentation'))
