"""Firebase Cloud Messaging."""

from dscms4.fcm.download import notify as notify_download
from dscms4.fcm.news import notify as notify_news


__all__ = ['notify_news']


def notify_chart(target: Union[GroupBaseChart, UserBaseChart]) -> None:
    """Notify via FCM about downloads."""