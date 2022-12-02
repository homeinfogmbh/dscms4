"""Downloads messaging."""

from logging import getLogger

from firebase_admin.messaging import BatchResponse

from cmslib import BaseChart
from comcatlib import URLCode
from comcatlib import multicast_base_chart


__all__ = ['notify']


def notify(base_chart: BaseChart) -> BatchResponse:
    """Notify via FCM about downloads."""

    getLogger('dscms4').info('Notifying about download chart: %s', base_chart)
    return multicast_base_chart(base_chart, URLCode.DOWNLOAD)
