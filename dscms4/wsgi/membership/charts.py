"""Memberships of a chart."""

from his import authenticated, authorized
from wsgilib import JSON

from dscms4.orm.content.group import GroupBaseChart
from dscms4.orm.content.terminal import TerminalBaseChart
from dscms4.orm.menu import MenuItemChart
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
    menu_items = tuple(get_menu_items(base_chart))
    menus = frozenset(menu_item.menu for menu_item in menu_items)
    json = {
        'groups': [group.id for group in tuple(get_groups(base_chart))],
        'terminals': [terminal.tid for terminal in get_terminals(base_chart)],
        'menu_items': [menu_item.id for menu_item in menu_items],
        'menus': [menu.id for menu in menus]}
    return JSON(json)


ROUTES = (
    ('GET', '/membership/chart/<int:ident>', list_, 'list_chart_containers'),)
