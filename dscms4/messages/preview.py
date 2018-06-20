"""Preview related messages."""

from dscms4.messages.common import DSCMS4Message

__all__ = ['Unauthorized']


class Unauthorized(DSCMS4Message):
    """Indicates that the respective preview access is not authorized."""

    STATUS = 401
