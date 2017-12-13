"""Management of configurations in terminals."""

from peewee import DoesNotExist

from wsgilib import JSON

from dscms4.messages.content.terminal import NoSuchTerminalConfiguration, \
    ConfigurationAddedToTerminal, ConfigurationAlreadyInTerminal, \
    ConfigurationDeletedFromTerminal
from dscms4.orm.content.terminal import TerminalConfiguration
from dscms4.wsgi.configuration import _get_configuration
from dscms4.wsgi.terminal import _get_terminal

__all__ = ['ROUTES']


def get(gid):
    """Returns a list of IDs of the configurations
    in the respective terminal.
    """

    return JSON([
        terminal_configuration.configuration.id for terminal_configuration
        in TerminalConfiguration.select().where(
            TerminalConfiguration.terminal == _get_terminal(gid))])


def add(gid, ident):
    """Adds the configuration to the respective terminal."""

    terminal = _get_terminal(gid)
    configuration = _get_configuration(ident)

    try:
        TerminalConfiguration.get(
            (TerminalConfiguration.terminal == terminal)
            & (TerminalConfiguration.configuration == configuration))
    except DoesNotExist:
        terminal_configuration = TerminalConfiguration()
        terminal_configuration.terminal = terminal
        terminal_configuration.configuration = configuration
        terminal_configuration.save()
        return ConfigurationAddedToTerminal()

    return ConfigurationAlreadyInTerminal()


def delete(gid, ident):
    """Deletes the configuration from the respective terminal."""

    try:
        terminal_configuration = TerminalConfiguration.get(
            (TerminalConfiguration.terminal == _get_terminal(gid))
            & (TerminalConfiguration.id == ident))
    except DoesNotExist:
        raise NoSuchTerminalConfiguration()

    terminal_configuration.delete_instance()
    return ConfigurationDeletedFromTerminal()


ROUTES = (
    ('/content/terminal/<int:gid>/configuration', 'GET', get),
    ('/content/terminal/<int:gid>/configuration', 'POST', add),
    ('/content/terminal/<int:gid>/configuration/<int:ident>', 'DELETE', delete)
)
