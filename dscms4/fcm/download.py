"""Downloads messaging."""

from typing import Optional

from firebase_admin.messaging import BatchResponse

from cmslib import BaseChart
from comcatlib import Menu
from comcatlib import URLCode
from comcatlib import get_tokens
from comcatlib import multicast_base_chart

from dscms4.fcm.common import affected_users, is_in_menu


__all__ = ['notify']


def notify(base_chart: BaseChart) -> Optional[BatchResponse]:
    """Notify via FCM about downloads."""

    if not is_in_menu(base_chart, Menu.DOCUMENTS):
        return

    return multicast_base_chart(
        base_chart.chart,
        URLCode.DOWNLOAD,
        get_tokens(set(affected_users(base_chart)))
    )
