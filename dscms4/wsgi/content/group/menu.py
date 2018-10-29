"""Management of menus in groups."""

from his import authenticated, authorized
from wsgilib import JSON

from dscms4.messages.content import ContentAdded
from dscms4.messages.content import ContentDeleted
from dscms4.messages.content import ContentExists
from dscms4.messages.content import NoSuchContent
from dscms4.orm.content.group import GroupMenu
from dscms4.wsgi.group.group import get_group
from dscms4.wsgi.menu.menu import get_menu


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(gid):
    """Returns a list of IDs of the menus in the respective group."""

    group = get_group(gid)
    return JSON([
        group_menu.menu.id for group_menu in GroupMenu.select().where(
            GroupMenu.group == group)])


@authenticated
@authorized('dscms4')
def add(gid, ident):
    """Adds the menu to the respective group."""

    group = get_group(gid)
    menu = get_menu(ident)

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


@authenticated
@authorized('dscms4')
def delete(gid, ident):
    """Deletes the menu from the respective group."""

    group = get_group(gid)
    menu = get_menu(ident)

    try:
        group_menu = GroupMenu.get(
            (GroupMenu.group == group) & (GroupMenu.menu == menu))
    except GroupMenu.DoesNotExist:
        raise NoSuchContent()

    group_menu.delete_instance()
    return ContentDeleted()


ROUTES = (
    ('GET', '/content/group/<int:gid>/menu', get, 'list_group_menus'),
    ('POST', '/content/group/<int:gid>/menu/<int:ident>', add,
     'add_group_menu'),
    ('DELETE', '/content/group/<int:gid>/menu/<int:ident>', delete,
     'delete_group_menu'))
