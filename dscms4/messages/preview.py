"""Preview related messages."""

from dscms4.messages.common import DSCMS4Message

__all__ = ['Unauthorized', 'InvalidTokenType', 'NoSuchObject']


class Unauthorized(DSCMS4Message):
    """Indicates that the respective preview access is not authorized."""

    STATUS = 401


class InvalidTokenType(DSCMS4Message):
    """Indicates that the respective preview access is not authorized."""

    STATUS = 400


class NoSuchObject(DSCMS4Message):
    """Indicates that the respective object could not be found."""

    STATUS = 404
