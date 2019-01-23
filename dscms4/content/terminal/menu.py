"""Management of menus in terminals."""

from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_EXISTS
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.content.terminal import TerminalMenu
from his import authenticated, authorized
from wsgilib import JSON

from dscms4.menu.menu import get_menu
from dscms4.terminal import get_terminal


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(gid):
    """Returns a list of IDs of the menus in the respective terminal."""

    return JSON([
        terminal_menu.menu.id for terminal_menu in TerminalMenu.select().where(
            TerminalMenu.terminal == get_terminal(gid))])


@authenticated
@authorized('dscms4')
def add(gid, ident):
    """Adds the menu to the respective terminal."""

    terminal = get_terminal(gid)
    menu = get_menu(ident)

    try:
        TerminalMenu.get(
            (TerminalMenu.terminal == terminal) & (TerminalMenu.menu == menu))
    except TerminalMenu.DoesNotExist:
        terminal_menu = TerminalMenu()
        terminal_menu.terminal = terminal
        terminal_menu.menu = menu
        terminal_menu.save()
        return CONTENT_ADDED

    return CONTENT_EXISTS


@authenticated
@authorized('dscms4')
def delete(gid, ident):
    """Deletes the menu from the respective terminal."""

    terminal = get_terminal(gid)
    menu = get_menu(ident)

    try:
        terminal_menu = TerminalMenu.get(
            (TerminalMenu.terminal == terminal) & (TerminalMenu.menu == menu))
    except TerminalMenu.DoesNotExist:
        raise NO_SUCH_CONTENT

    terminal_menu.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/terminal/<int:gid>/menu', get, 'list_terminal_menus'),
    ('POST', '/content/terminal/<int:gid>/menu/<int:ident>', add,
     'add_terminal_menu'),
    ('DELETE', '/content/terminal/<int:gid>/menu/<int:ident>', delete,
     'delete_terminal_menu'))
