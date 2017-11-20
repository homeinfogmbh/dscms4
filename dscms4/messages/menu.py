"""Menu realted messages."""


from dscms4.messages.common import DSCMS4Message

__all__ = ['NoSuchMenu', 'InvalidMenuData']


class NoSuchMenu(DSCMS4Message):
    """Indicates that the requested menu does not exist."""

    STATUS = 404


class InvalidMenuData(DSCMS4Message):
    """Indicates that invalid menu data has been specified."""

    STATUS = 400
