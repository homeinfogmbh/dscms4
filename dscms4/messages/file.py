"""Messages for file handlers."""

from his.messages import locales, Message

__all__ = [
    'NoSuchFile',
    'FilesAdded',
    'FileExists',
    'FileDeleted']


class FileMessage(Message):
    """Base class for content related messages."""

    LOCALES = locales('/etc/dscms4.d/locales/file.ini')
    ABSTRACT = True


class NoSuchFile(FileMessage):
    """Indicates that the respective file does not exist."""

    STATUS = 404


class FilesAdded(FileMessage):
    """Indicates that the respective files were added."""

    STATUS = 201


class FileExists(FileMessage):
    """Indicates that the respective file already exists."""

    STATUS = 400


class FileDeleted(FileMessage):
    """Indicates that the respective file was deleted."""

    STATUS = 200
