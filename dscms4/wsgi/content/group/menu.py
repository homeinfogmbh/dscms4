"""Management of menus in groups."""

from peewee import DoesNotExist

from wsgilib import JSON

from dscms4.messages.content.group import NoSuchGroupMenu, MenuAddedToGroup, \
    MenuAlreadyInGroup, MenuDeletedFromGroup
from dscms4.orm.content.group import GroupMenu
from dscms4.wsgi.group import _get_group
from dscms4.wsgi.menu import _get_menu

__all__ = ['get_group_menus', 'add_group_menu', 'delete_group_menu']


def get_group_menus(gid):
    """Returns a list of IDs of the menus in the respective group."""

    return JSON([group_menu.menu.id for group_menu in GroupMenu.select().where(
        GroupMenu.group == _get_group(gid))])


def add_group_menu(gid, ident):
    """Adds the menu to the respective group."""

    group = _get_group(gid)
    menu = _get_menu(ident)

    try:
        GroupMenu.get(
            (GroupMenu.group == group) & (GroupMenu.menu == menu))
    except DoesNotExist:
        group_menu = GroupMenu()
        group_menu.group = group
        group_menu.menu = menu
        group_menu.save()
        return MenuAddedToGroup()

    return MenuAlreadyInGroup()


def delete_group_menu(gid, ident):
    """Deletes the menu from the respective group."""

    try:
        group_menu = GroupMenu.get(
            (GroupMenu.group == _get_group(gid)) & (GroupMenu.id == ident))
    except DoesNotExist:
        raise NoSuchGroupMenu()

    group_menu.delete_instance()
    return MenuDeletedFromGroup()
