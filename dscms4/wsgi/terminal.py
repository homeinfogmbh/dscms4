"""Terminal-related requests."""

from flask import request

from his import CUSTOMER, authenticated, authorized
from his.messages import InvalidData
from peeweeplus import async_select
from terminallib import Terminal
from wsgilib import JSON, XML

from dscms4.asynclib import async_dict
from dscms4.exceptions import AmbiguousConfigurationsError
from dscms4.exceptions import NoConfigurationFound
from dscms4.messages.presentation import NoConfigurationAssigned
from dscms4.messages.presentation import AmbiguousConfigurations
from dscms4.messages.terminal import NoSuchTerminal
from dscms4.orm.content.terminal import TerminalBaseChart
from dscms4.orm.content.terminal import TerminalConfiguration
from dscms4.orm.content.terminal import TerminalMenu
from dscms4.paging import page, pages
from dscms4.presentation import Presentation


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


def json_terminals(terminals):
    """Converts the respective terminals to JSON."""

    def keyfunc(terminal):
        return terminal.tid

    def valfunc(terminal):
        return TerminalContent(terminal).to_json(asynchronous=False)

    return async_dict(terminals, keyfunc, valfunc)


@authenticated
@authorized('dscms4')
def list_():
    """Lists all terminals of the respective customer."""

    expression = Terminal.customer == CUSTOMER.id
    settings = Settings.for_customer(CUSTOMER.id)

    if not settings.show_testing_terminals:
        expression &= Terminal.testing == 0

    terminals = Terminal.select().where(expression)

    try:
        size = int(request.args['size'])
    except KeyError:
        size = None
    except ValueError:
        raise InvalidData(parameter='size')

    if size is not None:
        try:
            pageno = int(request.args['page'])
        except KeyError:
            pageno = None
        except ValueError:
            raise InvalidData(parameter='page')

        if pageno is not None:
            return JSON([terminal.to_json(short=True) for terminal in page(
                terminals, size, pageno)])

        return JSON({'pages': pages(terminals, size)})

    if 'assoc' in request.args:
        asynchronous = 'noasync' not in request.args

        if asynchronous and 'asyncdict' in request.args:
            return JSON(json_terminals(terminals))

        return JSON({
            terminal.tid: TerminalContent(terminal).to_json(
                asynchronous=asynchronous)
            for terminal in terminals})

    return JSON([terminal.to_json(short=True) for terminal in terminals])


@authenticated
@authorized('dscms4')
@with_terminal
def get(terminal):
    """Returns the respective terminal."""

    return JSON(terminal.to_json())


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
    except AmbiguousConfigurationsError:
        return AmbiguousConfigurations()
    except NoConfigurationFound:
        return NoConfigurationAssigned()

    return XML(presentation_dom)


class TerminalContent:
    """Represents content of a terminal."""

    def __init__(self, terminal):
        """Sets the terminal."""
        self.terminal = terminal

    @property
    def charts(self):
        """Yields the terminal's charts."""
        for terminal_base_chart in TerminalBaseChart.select().where(
                TerminalBaseChart.terminal == self.terminal):
            yield terminal_base_chart.to_json()

    @property
    def configurations(self):
        """Yields the terminal's configurations."""
        for terminal_configuration in TerminalConfiguration.select().where(
                TerminalConfiguration.terminal == self.terminal):
            yield terminal_configuration.to_json()

    @property
    def menus(self):
        """Yields the terminal's menus."""
        for terminal_menu in TerminalMenu.select().where(
                TerminalMenu.terminal == self.terminal):
            yield terminal_menu.to_json()

    def content(self, asynchronous=True):
        """Returns content."""
        if asynchronous:
            return async_select(
                charts=self.charts, configurations=self.configurations,
                menus=self.menus)

        return {
            'charts': list(self.charts),
            'configurations': list(self.configurations),
            'menus': list(self.menus)}

    def to_json(self, asynchronous=True):
        """Returns the terminal and its content as a JSON-ish dict."""
        address = self.terminal.address
        json = {'address': address.to_json()} if address else {}
        json['content'] = self.content(asynchronous=asynchronous)
        return json


ROUTES = (
    ('GET', '/terminal', list_, 'list_terminals'),
    ('GET', '/terminal/<int:tid>', get, 'get_terminal'),
    ('GET', '/terminal/<int:tid>/presentation', get_presentation,
     'get_terminal_presentation'))
