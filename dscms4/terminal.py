"""Terminal-related requests."""

from flask import request

from cmslib.exceptions import AmbiguousConfigurationsError
from cmslib.exceptions import NoConfigurationFound
from cmslib.messages.presentation import NO_CONFIGURATION_ASSIGNED
from cmslib.messages.presentation import AMBIGUOUS_CONFIGURATIONS
from cmslib.messages.terminal import NO_SUCH_TERMINAL
from cmslib.orm.charts import BaseChart
from cmslib.orm.content.terminal import TerminalBaseChart
from cmslib.orm.content.terminal import TerminalConfiguration
from cmslib.orm.content.terminal import TerminalMenu
from cmslib.orm.settings import Settings
from cmslib.presentation.terminal import Presentation
from his import CUSTOMER, authenticated, authorized
from terminallib import Terminal
from wsgilib import Browser, JSON, XML


__all__ = ['get_terminal', 'ROUTES']


BROWSER = Browser()


def get_terminal(tid):
    """Returns the respective terminal."""

    try:
        return Terminal.get(
            (Terminal.tid == tid) & (Terminal.customer == CUSTOMER.id))
    except Terminal.DoesNotExist:
        raise NO_SUCH_TERMINAL


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
    settings = Settings.for_customer(CUSTOMER.id)

    if not settings.show_testing_terminals:
        expression &= Terminal.testing == 0

    terminals = Terminal.select().where(expression)

    if BROWSER.wanted:
        if BROWSER.info:
            return BROWSER.pages(terminals).to_json()

        return JSON([
            terminal.to_json(short=True) for terminal
            in BROWSER.browse(terminals)])

    if 'assoc' in request.args:
        return JSON({
            terminal.tid: TerminalContent(terminal).to_json()
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
        return AMBIGUOUS_CONFIGURATIONS
    except NoConfigurationFound:
        return NO_CONFIGURATION_ASSIGNED

    return XML(presentation_dom)


class TerminalContent:
    """Represents content of a terminal."""

    def __init__(self, terminal):
        """Sets the terminal."""
        self.terminal = terminal

    @property
    def charts(self):
        """Yields the terminal's charts."""
        for terminal_base_chart in TerminalBaseChart.select().join(
                BaseChart).where(
                    (TerminalBaseChart.terminal == self.terminal)
                    & (BaseChart.trashed == 0)):
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

    def content(self):
        """Returns content."""
        return {
            'charts': list(self.charts),
            'configurations': list(self.configurations),
            'menus': list(self.menus)}

    def to_json(self):
        """Returns the terminal and its content as a JSON-ish dict."""
        address = self.terminal.address
        json = {'address': address.to_json()} if address else {}
        json['content'] = self.content()
        return json


ROUTES = (
    ('GET', '/terminal', list_, 'list_terminals'),
    ('GET', '/terminal/<int:tid>', get, 'get_terminal'),
    ('GET', '/terminal/<int:tid>/presentation', get_presentation,
     'get_terminal_presentation'))
