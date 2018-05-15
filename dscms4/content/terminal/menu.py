"""Terminal menus."""

from dscms4.content.common import ContentInformation, terminal_groups
from dscms4.content.group.menu import accumulated_menus as _accumulated_menus
from dscms4.orm.content.terminal import TerminalMenu

__all__ = ['menus', 'accumulated_menus']


def menus(terminal):
    """Yields terminal menus of the terminal."""

    for terminal_menu in TerminalMenu.select().where(
            TerminalMenu.terminal == terminal):
        yield ContentInformation(terminal, terminal_menu.menu)


def accumulated_menus(terminal):
    """Yields accumulated menus of the terminal."""

    yield from menus(terminal)

    for group in terminal_groups(terminal):
        yield from _accumulated_menus(group)
