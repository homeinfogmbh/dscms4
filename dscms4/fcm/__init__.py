"""Firebase Cloud Messaging."""

from typing import Optional

from firebase_admin.messaging import BatchResponse

from cmslib import BaseChart
from comcatlib import Menu, multicast_customer_event as notify_customer_event

from dscms4.fcm.common import is_in_menu
from dscms4.fcm.download import notify as notify_download
from dscms4.fcm.news import notify as notify_news


__all__ = ['notify_base_chart', 'notify_customer_event']


def notify_base_chart(base_chart: BaseChart) -> Optional[BatchResponse]:
    """Notify via FCM about base chart-related changes."""

    if is_in_menu(base_chart, Menu.DOCUMENTS):
        return notify_download(base_chart)

    if is_in_menu(base_chart, Menu.NEWS):
        return notify_news(base_chart)

    return None
