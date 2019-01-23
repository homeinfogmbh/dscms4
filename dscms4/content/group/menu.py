"""Management of menus in groups."""

from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_EXISTS
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.content.group import GroupMenu
from his import authenticated, authorized
from wsgilib import JSON

from dscms4.group.group import get_group
from dscms4.menu.menu import get_menu


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
        return CONTENT_ADDED

    return CONTENT_EXISTS


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
        raise NO_SUCH_CONTENT

    group_menu.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/group/<int:gid>/menu', get, 'list_group_menus'),
    ('POST', '/content/group/<int:gid>/menu/<int:ident>', add,
     'add_group_menu'),
    ('DELETE', '/content/group/<int:gid>/menu/<int:ident>', delete,
     'delete_group_menu'))
