"""Memberships of a chart."""

from his import authenticated, authorized
from wsgilib import JSON

from cmslib.orm.content.group import GroupBaseChart
from cmslib.orm.content.terminal import TerminalBaseChart
from cmslib.orm.menu import MenuItemChart

from dscms4.wsgi.charts import get_chart


__all__ = ['ROUTES']


def get_groups(ident):
    """Returns the groups, this base chart is member of."""

    for group_base_chart in GroupBaseChart.select().where(
            GroupBaseChart.base_chart == ident):
        yield group_base_chart.group


def get_terminals(ident):
    """Returns the groups, this base chart is member of."""

    for terminal_base_chart in TerminalBaseChart.select().where(
            TerminalBaseChart.base_chart == ident):
        yield terminal_base_chart.terminal


def get_menu_items(ident):
    """Returns the groups, this base chart is member of."""

    for menu_item_chart in MenuItemChart.select().where(
            MenuItemChart.base_chart == ident):
        yield menu_item_chart.menu_item


@authenticated
@authorized('dscms4')
def list_(ident):
    """Lists the chart's containers."""

    chart = get_chart(ident)
    base_chart = chart.base
    json = {
        'groups': [
            {
                'group': group_base_chart.group.id,
                'member': group_base_chart.id
            }
            for group_base_chart in GroupBaseChart.select().where(
                GroupBaseChart.base_chart == base_chart)],
        'terminals': [
            {
                'terminal': terminal_base_chart.terminal.tid,
                'member': terminal_base_chart.id
            }
            for terminal_base_chart in TerminalBaseChart.select().where(
                TerminalBaseChart.base_chart == base_chart)],
        'menus': [
            {
                'menu': menu_item_chart.menu_item.menu.id,
                'menuItem': menu_item_chart.menu_item.id,
                'member': menu_item_chart.id
            }
            for menu_item_chart in MenuItemChart.select().where(
                MenuItemChart.base_chart == base_chart)]
    }
    return JSON(json)


ROUTES = (
    ('GET', '/membership/charts/<int:ident>', list_, 'list_chart_containers'),)
