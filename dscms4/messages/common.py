"""Common messages."""

from his.messages import locales, Message

__all__ = ['DSCMS4Message', 'InvalidId', 'NoIdSpecified']


class DSCMS4Message(Message):
    """Basic real estates message."""

    LOCALES = locales('/etc/dscms4.d/locales/dscms4.ini')


class InvalidId(DSCMS4Message):
    """Indicates that the respective ID is invalid."""

    STATUS = 400


class NoIdSpecified(DSCMS4Message):
    """Indicates that no ID was specified."""

    STATUS = 400
