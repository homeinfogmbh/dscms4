"""Management of menus in groups."""

from cmslib.functions.group import get_group
from cmslib.functions.menu import get_menu
from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_EXISTS
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.content.group import GroupMenu
from his import authenticated, authorized
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(gid: int) -> JSON:
    """Returns a list of IDs of the menus in the respective group."""

    group = get_group(gid)
    return JSON([
        group_menu.menu.id for group_menu in GroupMenu.select().where(
            GroupMenu.group == group)])


@authenticated
@authorized('dscms4')
def add(gid: int, ident: int) -> JSONMessage:
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
def delete(gid: int, ident: int) -> JSONMessage:
    """Deletes the menu from the respective group."""

    group = get_group(gid)
    menu = get_menu(ident)

    try:
        group_menu = GroupMenu.get(
            (GroupMenu.group == group) & (GroupMenu.menu == menu))
    except GroupMenu.DoesNotExist:
        return NO_SUCH_CONTENT

    group_menu.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/group/<int:gid>/menu', get),
    ('POST', '/content/group/<int:gid>/menu/<int:ident>', add),
    ('DELETE', '/content/group/<int:gid>/menu/<int:ident>', delete)
)
