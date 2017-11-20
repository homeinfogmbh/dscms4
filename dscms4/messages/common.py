"""Common messages."""


from his.api.messages import locales, HISMessage

__all__ = ['DSCMS4Message', 'NoIdSpecified', 'InvalidId']


@locales('/etc/his.d/locale/dscms4.ini')
class DSCMS4Message(HISMessage):
    """Basic real estates message."""

    pass


class NoIdSpecified(DSCMS4Message):
    """Indicates that an ID was missing."""

    STATUS = 422


class InvalidId(DSCMS4Message):
    """Indicates that a specified ID had an invalid value."""

    STATUS = 406
