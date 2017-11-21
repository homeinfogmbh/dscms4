"""Menu realted messages."""

from dscms4.messages.common import DSCMS4Message

__all__ = [
    # Menus.
    'NoMenuSpecified',
    'NoSuchMenu',
    'InvalidMenuData',
    'MenuAdded',
    'NoSuchMenuItem',
    # Menu items.
    'NoMenuItemSpecified',
    'NoSuchMenuItem',
    'MenuItemAdded',
    'MenuItemDeleted']


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


class MenuItemDeleted(DSCMS4Message):
    """Indicates that the respective menu item was successfully deleted."""

    STATUS = 400
