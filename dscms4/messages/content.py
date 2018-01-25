"""Messages for content handlers."""

from his.messages import locales, Message

__all__ = [
    'NoTypeSpecified',
    'InvalidContentType',
    'ContentAdded',
    'ContentDeleted']


class ContentMessage(Message):
    """Base class for content related messages."""

    LOCALES = locales('/etc/dscms4.d/locales/content.ini')
    ABSTRACT = True


class NoTypeSpecified(ContentMessage):
    """Indicates that no content type was specified."""

    STATUS = 400


class InvalidContentType(ContentMessage):
    """Indicates that an invalid content type has bee specified."""

    STATUS = 400


class ContentAdded(ContentMessage):
    """Indicates that the respective content was added."""

    STATUS = 201


class ContentDeleted(ContentMessage):
    """Indicates that the respective content was deleted."""

    STATUS = 200
