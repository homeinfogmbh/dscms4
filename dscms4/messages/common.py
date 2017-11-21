"""Common messages."""


from his.api.messages import locales, HISMessage

__all__ = ['DSCMS4Message']


@locales('/etc/his.d/locale/dscms4.ini')
class DSCMS4Message(HISMessage):
    """Basic real estates message."""

    pass
