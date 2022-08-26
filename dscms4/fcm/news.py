"""News messaging."""

from typing import Iterable, Union

from cmslib import BaseChart, GroupBaseChart
from comcatlib import GroupMemberUser
from comcatlib import Menu
from comcatlib import MenuBaseChart
from comcatlib import URLCode
from comcatlib import User
from comcatlib import UserBaseChart
from comcatlib import expand_groups
from comcatlib import get_tokens
from comcatlib import multicast_chart


__all__ = ['notify_news']


def notify_news(target: Union[GroupBaseChart, UserBaseChart]) -> None:
    """Notify via FCM about news."""

    if not is_news(target.base_chart):
        return

    multicast_chart(
        target.chart,
        URLCode.NEWS,
        get_tokens(set(affected_users(target)))
    )


def is_news(base_chart: Union[BaseChart, int]) -> bool:
    """Determine whether the given base chart is a news chart."""

    try:
        MenuBaseChart.get(
            (MenuBaseChart.base_chart == base_chart)
            & (MenuBaseChart.menu == Menu.NEWS)
        )
    except MenuBaseChart.DoesNotEixst:
        return False

    return True


def affected_users(
        target: Union[GroupBaseChart, UserBaseChart]
) -> Iterable[Union[User, int]]:
    """Return a set of users affected by the
    change to the respective chart mapping.
    """

    if isinstance(target, UserBaseChart):
        return {UserBaseChart.user}

    for member in GroupMemberUser.select().where(
            GroupMemberUser.group << expand_groups(target.group)
    ):
        yield member.user
