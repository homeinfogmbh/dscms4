"""Menu realted messages."""

from dscms4.messages.common import DSCMS4Message

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
    'DifferentParentsError',
    'NoSuchMenuItemChart',
    'MenuItemChartAdded',
    'MenuItemChartDeleted',
    'DifferentMenuItemsError',
    'MenuItemChartsSorted']


class NoMenuSpecified(DSCMS4Message):
    """Indicates that no menu was specified."""

    STATUS = 400


class NoSuchMenu(DSCMS4Message):
    """Indicates that the requested menu does not exist."""

    STATUS = 404


class InvalidMenuData(DSCMS4Message):
    """Indicates that invalid menu data has been specified."""

    STATUS = 400


class MenuAdded(DSCMS4Message):
    """Indicates that the menu was successfully added."""

    STATUS = 201


class MenuPatched(DSCMS4Message):
    """Indicates that the menu was successfully patched."""

    STATUS = 200


class MenuDeleted(DSCMS4Message):
    """Indicates that the menu was successfully deleted."""

    STATUS = 200


class NoMenuItemSpecified(DSCMS4Message):
    """Indicates that no menu item was specified."""

    STATUS = 400


class NoSuchMenuItem(DSCMS4Message):
    """Indicates that the requested menu item does not exist."""

    STATUS = 404


class MenuItemAdded(DSCMS4Message):
    """Indicates that the respective menu item was successfully added."""

    STATUS = 201


class MenuItemPatched(DSCMS4Message):
    """Indicates that the respective menu item was successfully patched."""

    STATUS = 200


class MenuItemDeleted(DSCMS4Message):
    """Indicates that the respective menu item was successfully deleted."""

    STATUS = 200


class MenuItemsSorted(DSCMS4Message):
    """Indicates that the respective menu items have been sorted."""

    STATUS = 200


class DifferentMenusError(DSCMS4Message):
    """Indicates that the respective menu items are in separate menus."""

    STATUS = 400


class DifferentParentsError(DSCMS4Message):
    """Indicates that the respective menu items have different parents."""

    STATUS = 400


class NoSuchMenuItemChart(DSCMS4Message):
    """Indicates that the respective menu item chart does not exist."""

    STATUS = 404


class MenuItemChartAdded(DSCMS4Message):
    """Indicates that the respective menu
    item chart has successfully been added.
    """

    STATUS = 200


class MenuItemChartDeleted(DSCMS4Message):
    """Indicates that the respective menu
    item chart has successfully been deleted.
    """

    STATUS = 200


class DifferentMenuItemsError(DSCMS4Message):
    """Indicates that the respective menu
    item charts are in separate menu items.
    """

    STATUS = 400


class MenuItemChartsSorted(DSCMS4Message):
    """Indicates that the respective menu item charts have been sorted."""

    STATUS = 200
