"""Common messages."""


from his.api.messages import locales, HISMessage

__all__ = ['DSCMS4Message', 'InvalidId', 'NoIdSpecified']


@locales('/etc/his.d/locale/dscms4.ini')
class DSCMS4Message(HISMessage):
    """Basic real estates message."""

    pass


class InvalidId(DSCMS4Message):
    """Indicates that the respective ID is invalid."""

    STATUS = 400


class NoIdSpecified(DSCMS4Message):
    """Indicates that no ID was specified."""

    STATUS = 400
