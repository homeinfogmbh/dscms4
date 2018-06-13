"""Messages for content handlers."""

from his.messages import Message

__all__ = [
    'NoSuchContent',
    'NoTypeSpecified',
    'InvalidContentType',
    'ContentAdded',
    'ContentExists',
    'ContentDeleted',
    'NoConfigurationAssigned']


class ContentMessage(Message):
    """Base class for content related messages."""

    LOCALES = '/etc/dscms4.d/locales/content.ini'


class NoSuchContent(ContentMessage):
    """Indicates that the respective content does not exist."""

    STATUS = 404


class NoTypeSpecified(ContentMessage):
    """Indicates that no content type was specified."""

    STATUS = 400


class InvalidContentType(ContentMessage):
    """Indicates that an invalid content type has bee specified."""

    STATUS = 400


class ContentAdded(ContentMessage):
    """Indicates that the respective content was added."""

    STATUS = 201


class ContentExists(ContentMessage):
    """Indicates that the respective content already exists."""

    STATUS = 400


class ContentDeleted(ContentMessage):
    """Indicates that the respective content was deleted."""

    STATUS = 200


class NoConfigurationAssigned(ContentMessage):
    """Indicates that no configuration has been
    assigned to the respective presentation.
    """

    STATUS = 404
