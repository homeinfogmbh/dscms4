"""Management of menus in groups."""

from wsgilib import JSON

from dscms4.messages.content import NoSuchContent, ContentAdded, \
    ContentExists, ContentDeleted
from dscms4.orm.content.group import GroupMenu
from dscms4.wsgi.group import get_group
from dscms4.wsgi.menu import get_menu

__all__ = ['ROUTES']


def get(gid):
    """Returns a list of IDs of the menus in the respective group."""

    return JSON([group_menu.menu.id for group_menu in GroupMenu.select().where(
        GroupMenu.group == _get_group(gid))])


def add(gid, ident):
    """Adds the menu to the respective group."""

    group = _get_group(gid)
    menu = _get_menu(ident)

    try:
        GroupMenu.get(
            (GroupMenu.group == group) & (GroupMenu.menu == menu))
    except GroupMenu.DoesNotExist:
        group_menu = GroupMenu()
        group_menu.group = group
        group_menu.menu = menu
        group_menu.save()
        return ContentAdded()

    return ContentExists()


def delete(gid, ident):
    """Deletes the menu from the respective group."""

    try:
        group_menu = GroupMenu.get(
            (GroupMenu.group == _get_group(gid)) & (GroupMenu.id == ident))
    except GroupMenu.DoesNotExist:
        raise NoSuchContent()

    group_menu.delete_instance()
    return ContentDeleted()


ROUTES = (
    ('GET', '/content/group/<int:gid>/menu', get, 'list_group_menus'),
    ('POST', '/content/group/<int:gid>/menu', add, 'add_group_menu'),
    ('DELETE', '/content/group/<int:gid>/menu/<int:ident>', delete,
     'delete_group_menu'))
