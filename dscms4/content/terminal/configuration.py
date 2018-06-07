"""Terminal configurations."""

from dscms4.content.common import ContentInformation, terminal_groups
from dscms4.content.exceptions import NoConfigurationFound
from dscms4.content.group.configuration import \
    first_configuration as _first_configuration
from dscms4.orm.content.terminal import TerminalConfiguration

__all__ = ['configurations', 'first_configuration']


def configurations(terminal):
    """Yields configurations of the terminal."""

    for terminal_configuration in TerminalConfiguration.select().where(
            TerminalConfiguration.terminal == terminal):
        yield ContentInformation(
            terminal, terminal_configuration.configuration)


def first_configuration(terminal):
    """Yields accumulated configurations for the terminal."""

    for configuration in configurations(terminal):
        return configuration

    for group in terminal_groups(terminal):
        return _first_configuration(group)

    raise NoConfigurationFound()
