"""Media related messages."""

from his.messages import locales, Message

__all__ = [
    'NoSuchMediaFile',
    'QuotaExceeded',
    'MediaFileAdded',
    'MediaFileDeleted']


class MediaMessage(Message):
    """Base for media file related messages."""

    LOCALES = locales('/etc/dscms4.d/locales/media.ini')
    ABSTRACT = True


class NoSuchMediaFile(MediaMessage):
    """Indicates that the respective media file does not exist."""

    STATUS = 404


class QuotaExceeded(MediaMessage):
    """Indicates that the user's quota has been exceeded."""

    STATUS = 403


class MediaFileAdded(MediaMessage):
    """Indicates that the media files was stored successfully."""

    STATUS = 201


class MediaFileDeleted(MediaMessage):
    """Indicates that the respective media file was successfully deleted."""

    STATUS = 200
