"""Common functions."""

from typing import Iterable, Union

from cmslib import BaseChart, GroupBaseChart
from comcatlib import GroupMemberUser
from comcatlib import Menu
from comcatlib import MenuBaseChart
from comcatlib import User
from comcatlib import UserBaseChart
from comcatlib import expand_groups


__all__ = ['affected_users', 'is_in_menu']


def affected_users(
        base_chart: Union[BaseChart, int]
) -> Iterable[Union[User, int]]:
    """Return a set of users affected by the
    change to the respective chart mapping.
    """

    for user_base_chart in UserBaseChart.select().where(
            UserBaseChart.base_chart == base_chart
    ):
        yield user_base_chart.user

    for member in GroupMemberUser.select().where(
            GroupMemberUser.group << expand_groups({
                group_base_chart.group for
                group_base_chart in GroupBaseChart.select().where(
                    GroupBaseChart.base_chart == base_chart
                )
            })
    ):
        yield member.user


def is_in_menu(base_chart: Union[BaseChart, int], menu: Menu) -> bool:
    """Determine whether the given base chart is a news chart."""

    try:
        MenuBaseChart.get(
            (MenuBaseChart.base_chart == base_chart)
            & (MenuBaseChart.menu == menu)
        )
    except MenuBaseChart.DoesNotEixst:
        return False

    return True
