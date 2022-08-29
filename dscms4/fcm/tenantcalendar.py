"""Tenant calendar events messaging."""

from firebase_admin.messaging import BatchResponse

from cmslib import BaseChart
from comcatlib import URLCode
from comcatlib import get_tokens
from comcatlib import multicast_base_chart

from dscms4.fcm.common import affected_users


__all__ = ['notify']


def notify(user_event: UserEvent) -> BatchResponse:
    """Notify via FCM about downloads."""

    return multicast_message(
        [token.token for token in get_tokens(set(affected_users(user_event)))],
        url_code=URLCode.EVENTS,
        title=f'{APP_NAME}: {CAPTIONS[url_code]}',
        body=base_chart.title
    )
