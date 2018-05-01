"""Management of menus in terminals."""

from his import authenticated, authorized
from wsgilib import JSON

from dscms4.messages.content import NoSuchContent, ContentAdded, \
    ContentExists, ContentDeleted
from dscms4.orm.content.terminal import TerminalMenu
from dscms4.wsgi.terminal import get_terminal
from dscms4.wsgi.menu import get_menu

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
        return ContentAdded()

    return ContentExists()


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
        raise NoSuchContent()

    terminal_menu.delete_instance()
    return ContentDeleted()


ROUTES = (
    ('GET', '/content/terminal/<int:gid>/menu', get, 'list_terminal_menus'),
    ('POST', '/content/terminal/<int:gid>/menu/<int:ident>', add,
     'add_terminal_menu'),
    ('DELETE', '/content/terminal/<int:gid>/menu/<int:ident>', delete,
     'delete_terminal_menu'))
