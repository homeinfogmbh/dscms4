"""News messaging."""

from typing import Optional, Union

from firebase_admin.messaging import BatchResponse

from cmslib import GroupBaseChart
from comcatlib import Menu
from comcatlib import URLCode
from comcatlib import UserBaseChart
from comcatlib import get_tokens
from comcatlib import multicast_chart

from dscms4.fcm.common import affected_users, is_in_menu


__all__ = ['notify']


def notify(
        target: Union[GroupBaseChart, UserBaseChart]
) -> Optional[BatchResponse]:
    """Notify via FCM about news."""

    if not is_in_menu(target.base_chart, Menu.NEWS):
        return

    return multicast_chart(
        target.chart,
        URLCode.NEWS,
        get_tokens(set(affected_users(target)))
    )
