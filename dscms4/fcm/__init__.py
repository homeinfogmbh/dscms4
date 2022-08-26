"""Firebase Cloud Messaging."""

from cmslib import BaseChart
from comcatlib import Menu, User, evaluate_recipients

from dscms4.fcm.common import is_in_menu
from dscms4.fcm.download import notify as notify_download
from dscms4.fcm.news import notify as notify_news


__all__ = ['notify_base_chart']


def notify_base_chart(base_chart: BaseChart) -> list[User]:
    """Notify via FCM about base chart-related changes."""

    if is_in_menu(base_chart, Menu.DOCUMENTS):
        return list(evaluate_recipients(notify_download(base_chart)))

    if is_in_menu(base_chart, Menu.NEWS):
        return list(evaluate_recipients(notify_news(base_chart)))

    return []
