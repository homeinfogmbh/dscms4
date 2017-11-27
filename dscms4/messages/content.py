"""Messages for content handlers."""

__all__ = [
    'NoSuchBaseChart',
    'NoSuchConfiguration',
    'NoSuchMenu',
    'NoSuchTicker',
    'NoTypeSpecified',
    'InvalidContentType',
    'ContentAdded',
    'ContentDeleted']


class NoSuchBaseChart(DSCMS4Message):
    """Indicates that the respective base chart does not exist."""

    STATUS = 404


class NoSuchConfiguration(DSCMS4Message):
    """Indicates that the respective configuration does not exist."""

    STATUS = 404


class NoSuchMenu(DSCMS4Message):
    """Indicates that the respective menu does not exist."""

    STATUS = 404


class NoSuchTicker(DSCMS4Message):
    """Indicates that the respective ticker does not exist."""

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


class ContentDeleted(DSCMS4Message):
    """Indicates that the respective content was deleted."""

    STATUS = 200
