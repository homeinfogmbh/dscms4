"""Group memberships."""

from cmslib import Group, GroupConfiguration, GroupBaseChart, GroupMenu
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON


__all__ = ["ROUTES"]


@authenticated
@authorized("dscms4")
def list_group_configurations() -> JSON:
    """List group configurations."""

    return JSON(
        [
            gc.to_json()
            for gc in GroupConfiguration.select()
            .join(Group)
            .where(Group.customer == CUSTOMER.id)
        ]
    )


@authenticated
@authorized("dscms4")
def list_group_base_charts() -> JSON:
    """List group base charts."""

    return JSON(
        [
            gbc.to_json()
            for gbc in GroupBaseChart.select()
            .join(Group)
            .where(Group.customer == CUSTOMER.id)
        ]
    )


@authenticated
@authorized("dscms4")
def list_group_menus() -> JSON:
    """List group menus."""

    return JSON(
        [
            gm.to_json()
            for gm in GroupMenu.select()
            .join(Group)
            .where(Group.customer == CUSTOMER.id)
        ]
    )


ROUTES = [
    ("GET", "/membership/group/configuration", list_group_configurations),
    ("GET", "/membership/group/base-chart", list_group_base_charts),
    ("GET", "/membership/group/menu", list_group_menus),
]
