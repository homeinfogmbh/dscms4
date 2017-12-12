"""Management of menus in terminals."""

from peewee import DoesNotExist

from wsgilib import JSON

from dscms4.messages.content.terminal import NoSuchTerminalMenu, \
    MenuAddedToTerminal, MenuAlreadyInTerminal, MenuDeletedFromTerminal
from dscms4.orm.content.terminal import TerminalMenu
from dscms4.wsgi.terminal import _get_terminal
from dscms4.wsgi.menu import _get_menu

__all__ = ['get_terminal_menus', 'add_terminal_menu', 'delete_terminal_menu']


def get_terminal_menus(gid):
    """Returns a list of IDs of the menus in the respective terminal."""

    return JSON([
        terminal_menu.menu.id for terminal_menu in TerminalMenu.select().where(
        TerminalMenu.terminal == _get_terminal(gid))])


def add_terminal_menu(gid, ident):
    """Adds the menu to the respective terminal."""

    terminal = _get_terminal(gid)
    menu = _get_menu(ident)

    try:
        TerminalMenu.get(
            (TerminalMenu.terminal == terminal) & (TerminalMenu.menu == menu))
    except DoesNotExist:
        terminal_menu = TerminalMenu()
        terminal_menu.terminal = terminal
        terminal_menu.menu = menu
        terminal_menu.save()
        return MenuAddedToTerminal()

    return MenuAlreadyInTerminal()


def delete_terminal_menu(gid, ident):
    """Deletes the menu from the respective terminal."""

    try:
        terminal_menu = TerminalMenu.get(
            (TerminalMenu.terminal == _get_terminal(gid))
            & (TerminalMenu.id == ident))
    except DoesNotExist:
        raise NoSuchTerminalMenu()

    terminal_menu.delete_instance()
    return MenuDeletedFromTerminal()
