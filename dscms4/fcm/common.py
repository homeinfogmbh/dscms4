"""Common functions."""

from typing import Union

from cmslib import BaseChart
from comcatlib import Menu
from comcatlib import MenuBaseChart


__all__ = ['is_in_menu']


def is_in_menu(base_chart: Union[BaseChart, int], menu: Menu) -> bool:
    """Determine whether the given base chart is a news chart."""

    try:
        MenuBaseChart.get(
            (MenuBaseChart.base_chart == base_chart)
            & (MenuBaseChart.menu == menu)
        )
    except MenuBaseChart.DoesNotExist:
        return False

    return True
