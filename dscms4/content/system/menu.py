"""Management of menus in digital signage systems."""

from cmslib.functions.menu import get_menu
from cmslib.functions.system import get_system
from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_EXISTS
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.content.system import SystemMenu
from his import authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(system):
    """Returns a list of IDs of the menus in the respective system."""

    return JSON([
        system_menu.menu.id for system_menu in SystemMenu.select().where(
            SystemMenu.system == get_system(system))])


@authenticated
@authorized('dscms4')
def add(system, menu):
    """Adds the menu to the respective system."""

    system = get_system(system)
    menu = get_menu(menu)

    try:
        SystemMenu.get(
            (SystemMenu.system == system) & (SystemMenu.menu == menu))
    except SystemMenu.DoesNotExist:
        system_menu = SystemMenu()
        system_menu.system = system
        system_menu.menu = menu
        system_menu.save()
        return CONTENT_ADDED

    return CONTENT_EXISTS


@authenticated
@authorized('dscms4')
def delete(system, menu):
    """Deletes the menu from the respective system."""

    system = get_system(system)
    menu = get_menu(menu)

    try:
        system_menu = SystemMenu.get(
            (SystemMenu.system == system) & (SystemMenu.menu == menu))
    except SystemMenu.DoesNotExist:
        raise NO_SUCH_CONTENT

    system_menu.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/system/<int:system>/menu', get),
    ('POST', '/content/system/<int:system>/menu/<int:menu>', add),
    ('DELETE', '/content/system/<int:system>/menu/<int:menu>', delete)
)
