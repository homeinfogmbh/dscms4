"""Memberships of a chart."""

from cmslib.functions.charts import get_chart
from cmslib.orm.content.group import GroupBaseChart
from cmslib.orm.content.deployment import DeploymentBaseChart
from cmslib.orm.menu import MenuItemChart
from his import authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


def get_groups(base_chart):
    """Yields JSON representations of groups."""

    for group_base_chart in GroupBaseChart.select().where(
            GroupBaseChart.base_chart == base_chart):
        yield {
            'group': group_base_chart.group.id,
            'member': group_base_chart.id}


def get_deployments(base_chart):
    """Yields JSON representations of deployments."""

    for deployment_base_chart in DeploymentBaseChart.select().where(
            DeploymentBaseChart.base_chart == base_chart):
        yield {
            'deployment': deployment_base_chart.deployment,
            'member': deployment_base_chart.id}


def get_menus(base_chart):
    """Yields JSON representations of menus."""

    for menu_item_chart in MenuItemChart.select().where(
            MenuItemChart.base_chart == base_chart):
        yield {
            'menu': menu_item_chart.menu_item.menu.id,
            'menuItem': menu_item_chart.menu_item.id,
            'member': menu_item_chart.id}


@authenticated
@authorized('dscms4')
def list_(ident):
    """Lists the chart's containers."""

    chart = get_chart(ident)
    base_chart = chart.base
    json = {
        'groups': list(get_groups(base_chart)),
        'deployments': list(get_deployments(base_chart)),
        'menus': list(get_menus(base_chart))}
    return JSON(json)


ROUTES = (('GET', '/membership/charts/<int:ident>', list_),)
