"""Memberships of a chart."""

from typing import Iterator

from cmslib.functions.charts import get_base_chart
from cmslib.orm.content.group import GroupBaseChart
from cmslib.orm.content.deployment import DeploymentBaseChart
from cmslib.orm.menu import MenuItemChart
from his import authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


def get_groups(base_chart: int) -> Iterator[dict]:
    """Yields JSON representations of groups."""

    for record in GroupBaseChart.select().where(
            GroupBaseChart.base_chart == base_chart):
        yield {
            'group': record.group.id,
            'member': record.id
        }


def get_deployments(base_chart: int) -> Iterator[dict]:
    """Yields JSON representations of deployments."""

    for record in DeploymentBaseChart.select().where(
            DeploymentBaseChart.base_chart == base_chart):
        yield {
            'deployment': record.deployment,
            'member': record.id
        }


def get_menus(base_chart: int) -> Iterator[dict]:
    """Yields JSON representations of menus."""

    for record in MenuItemChart.select(cascade=True).where(
            MenuItemChart.base_chart == base_chart):
        yield {
            'menu': record.menu_item.menu.id,
            'menuItem': record.menu_item.id,
            'member': record.id
        }


@authenticated
@authorized('dscms4')
def list_(ident: int) -> JSON:
    """Lists the chart's containers."""

    base_chart = get_base_chart(ident)
    json = {
        'groups': list(get_groups(base_chart)),
        'deployments': list(get_deployments(base_chart)),
        'menus': list(get_menus(base_chart))
    }
    return JSON(json)


ROUTES = (('GET', '/membership/base_chart/<int:ident>', list_),)
