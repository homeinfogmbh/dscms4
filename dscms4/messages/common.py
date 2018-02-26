"""Common messages."""

from his.messages import locales, Message

__all__ = ['DSCMS4Message', 'InvalidId', 'NoIdSpecified', 'CircularReference']


class DSCMS4Message(Message):
    """Basic real estates message."""

    LOCALES = locales('/etc/dscms4.d/locales/common.ini')
    ABSTRACT = True


class InvalidId(DSCMS4Message):
    """Indicates that the respective ID is invalid."""

    STATUS = 400


class NoIdSpecified(DSCMS4Message):
    """Indicates that no ID was specified."""

    STATUS = 400


class CircularReference(DSCMS4Message):
    """Indicates that a circular reference was tried to be designed."""

    STATUS = 406
