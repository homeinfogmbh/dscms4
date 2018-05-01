"""Management of configurations in terminals."""

from his import authenticated, authorized
from wsgilib import JSON

from dscms4.messages.content import NoSuchContent, ContentAdded, \
    ContentExists, ContentDeleted
from dscms4.orm.content.terminal import TerminalConfiguration
from dscms4.wsgi.configuration import get_configuration
from dscms4.wsgi.terminal import get_terminal

__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(gid):
    """Returns a list of IDs of the configurations
    in the respective terminal.
    """

    return JSON([
        terminal_configuration.configuration.id for terminal_configuration
        in TerminalConfiguration.select().where(
            TerminalConfiguration.terminal == get_terminal(gid))])


@authenticated
@authorized('dscms4')
def add(gid, ident):
    """Adds the configuration to the respective terminal."""

    terminal = get_terminal(gid)
    configuration = get_configuration(ident)

    try:
        TerminalConfiguration.get(
            (TerminalConfiguration.terminal == terminal)
            & (TerminalConfiguration.configuration == configuration))
    except TerminalConfiguration.DoesNotExist:
        terminal_configuration = TerminalConfiguration()
        terminal_configuration.terminal = terminal
        terminal_configuration.configuration = configuration
        terminal_configuration.save()
        return ContentAdded()

    return ContentExists()


@authenticated
@authorized('dscms4')
def delete(gid, ident):
    """Deletes the configuration from the respective terminal."""

    terminal = get_terminal(gid)
    configuration = get_configuration(ident)

    try:
        terminal_configuration = TerminalConfiguration.get(
            (TerminalConfiguration.terminal == terminal)
            & (TerminalConfiguration.configuration == configuration))
    except TerminalConfiguration.DoesNotExist:
        raise NoSuchContent()

    terminal_configuration.delete_instance()
    return ContentDeleted()


ROUTES = (
    ('GET', '/content/terminal/<int:gid>/configuration', get,
     'list_terminal_configurations'),
    ('POST', '/content/terminal/<int:gid>/configuration/<int:ident>', add,
     'add_terminal_configuration'),
    ('DELETE', '/content/terminal/<int:gid>/configuration/<int:ident>', delete,
     'delete_terminal_configuration'))
