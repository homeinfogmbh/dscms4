"""Management of configurations in terminals."""

from cmslib.functions.configuration import get_configuration
from cmslib.functions.terminal import get_terminal
from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_EXISTS
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.content.terminal import TerminalConfiguration
from his import authenticated, authorized
from wsgilib import JSON


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
        return CONTENT_ADDED

    return CONTENT_EXISTS


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
        raise NO_SUCH_CONTENT

    terminal_configuration.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/terminal/<int:gid>/configuration', get,
     'list_terminal_configurations'),
    ('POST', '/content/terminal/<int:gid>/configuration/<int:ident>', add,
     'add_terminal_configuration'),
    ('DELETE', '/content/terminal/<int:gid>/configuration/<int:ident>', delete,
     'delete_terminal_configuration'))
