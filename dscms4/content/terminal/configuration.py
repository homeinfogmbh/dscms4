"""Terminal configurations."""

from dscms4.content.common import ContentInformation, terminal_groups
from dscms4.content.group.configuration import \
    accumulated_configurations as _accumulated_configurations
from dscms4.orm.content.terminal import TerminalConfiguration

__all__ = ['configurations', 'accumulated_configurations']


def configurations(terminal):
    """Yields configurations of the terminal."""

    for terminal_configuration in TerminalConfiguration.select().where(
            TerminalConfiguration.terminal == terminal):
        yield ContentInformation(
            terminal, terminal_configuration.configuration)


def accumulated_configurations(terminal):
    """Yields accumulated configurations for the terminal."""

    yield from configurations(terminal)

    for group in terminal_groups(terminal):
        yield from _accumulated_configurations(group)
