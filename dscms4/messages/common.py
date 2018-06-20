"""Common messages."""

from his.messages import Message

__all__ = ['DSCMS4Message', 'InvalidId', 'NoIdSpecified', 'CircularReference']


class DSCMS4Message(Message):
    """Basic real estates message."""

    DOMAIN = 'dscms4'


class InvalidId(DSCMS4Message):
    """Indicates that the respective ID is invalid."""

    STATUS = 400


class NoIdSpecified(DSCMS4Message):
    """Indicates that no ID was specified."""

    STATUS = 400


class CircularReference(DSCMS4Message):
    """Indicates that a circular reference was tried to be designed."""

    STATUS = 406
