"""Messages for content handlers."""

from dscms4.messages.common import DSCMS4Message

__all__ = [
    'NoSuchContent',
    'NoTypeSpecified',
    'InvalidContentType',
    'ContentAdded',
    'ContentExists',
    'ContentDeleted']


class NoSuchContent(DSCMS4Message):
    """Indicates that the respective content does not exist."""

    STATUS = 404


class NoTypeSpecified(DSCMS4Message):
    """Indicates that no content type was specified."""

    STATUS = 400


class InvalidContentType(DSCMS4Message):
    """Indicates that an invalid content type has bee specified."""

    STATUS = 400


class ContentAdded(DSCMS4Message):
    """Indicates that the respective content was added."""

    STATUS = 201


class ContentExists(DSCMS4Message):
    """Indicates that the respective content already exists."""

    STATUS = 400


class ContentDeleted(DSCMS4Message):
    """Indicates that the respective content was deleted."""

    STATUS = 200
