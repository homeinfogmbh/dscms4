"""Menu realted messages."""

from his.messages import locales, Message

__all__ = [
    'NoMenuSpecified',
    'NoSuchMenu',
    'InvalidMenuData',
    'MenuAdded',
    'NoSuchMenuItem',
    'NoMenuItemSpecified',
    'NoSuchMenuItem',
    'MenuItemAdded',
    'MenuItemDeleted',
    'MenuItemsSorted',
    'DifferentMenusError',
    'NoSuchMenuItemChart',
    'MenuItemChartAdded',
    'MenuItemChartDeleted',
    'DifferentMenuItemsError',
    'MenuItemChartsSorted']


class MenuMessage(Message):
    """Base class for menu related messages."""

    LOCALES = locales('/etc/dscms4.d/locales/menu.ini')
    ABSTRACT = True


class NoMenuSpecified(MenuMessage):
    """Indicates that no menu was specified."""

    STATUS = 400


class NoSuchMenu(MenuMessage):
    """Indicates that the requested menu does not exist."""

    STATUS = 404


class InvalidMenuData(MenuMessage):
    """Indicates that invalid menu data has been specified."""

    STATUS = 400


class MenuAdded(MenuMessage):
    """Indicates that the menu was successfully added."""

    STATUS = 201


class MenuPatched(MenuMessage):
    """Indicates that the menu was successfully patched."""

    STATUS = 200


class MenuDeleted(MenuMessage):
    """Indicates that the menu was successfully deleted."""

    STATUS = 200


class NoMenuItemSpecified(MenuMessage):
    """Indicates that no menu item was specified."""

    STATUS = 400


class NoSuchMenuItem(MenuMessage):
    """Indicates that the requested menu item does not exist."""

    STATUS = 404


class MenuItemAdded(MenuMessage):
    """Indicates that the respective menu item was successfully added."""

    STATUS = 201


class MenuItemPatched(MenuMessage):
    """Indicates that the respective menu item was successfully patched."""

    STATUS = 200


class MenuItemDeleted(MenuMessage):
    """Indicates that the respective menu item was successfully deleted."""

    STATUS = 200


class MenuItemsSorted(MenuMessage):
    """Indicates that the respective menu items have been sorted."""

    STATUS = 200


class DifferentMenusError(MenuMessage):
    """Indicates that the respective menu items are in separate menus."""

    STATUS = 400

class NoSuchMenuItemChart(MenuMessage):
    """Indicates that the respective menu item chart does not exist."""

    STATUS = 404

class MenuItemChartAdded(MenuMessage):
    """Indicates that the respective menu
    item chart has successfully been added.
    """

    STATUS = 200

class MenuItemChartDeleted(MenuMessage):
    """Indicates that the respective menu
    item chart has successfully been deleted.
    """

    STATUS = 200


class DifferentMenuItemsError(MenuMessage):
    """Indicates that the respective menu
    item charts are in separate menu items.
    """

    STATUS = 400


class MenuItemChartsSorted(MenuMessage):
    """Indicates that the respective menu item charts have been sorted."""

    STATUS = 200
