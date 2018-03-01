"""Content assigned to groups."""

from peewee import ForeignKeyField

from dscms4.orm.charts import BaseChart
from dscms4.orm.common import DSCMS4Model
from dscms4.orm.configuration import Configuration
from dscms4.orm.group import Group
from dscms4.orm.menu import Menu
from dscms4.orm.configuration import Ticker

__all__ = [
    'GroupBaseChart',
    'GroupConfiguration',
    'GroupMenu',
    'GroupTicker',
    'MODELS']


class GroupContent:
    """Common abstract content mapping."""

    group = ForeignKeyField(Group, column_name='group', on_delete='CASCADE')


class GroupBaseChart(DSCMS4Model, GroupContent):
    """Association of a base chart with a group."""

    class Meta:
        table_name = 'group_base_chart'

    chart = ForeignKeyField(
        BaseChart, column_name='base_chart', on_delete='CASCADE')


class GroupConfiguration(DSCMS4Model, GroupContent):
    """Association of a configuration with a group."""

    class Meta:
        table_name = 'group_configuration'

    configuration = ForeignKeyField(
        Configuration, column_name='configuration', on_delete='CASCADE')


class GroupMenu(DSCMS4Model, GroupContent):
    """Association of a menu with a group."""

    class Meta:
        table_name = 'group_menu'

    menu = ForeignKeyField(Menu, column_name='menu', on_delete='CASCADE')


class GroupTicker(DSCMS4Model, GroupContent):
    """Association of a ticker with a group."""

    class Meta:
        table_name = 'group_ticker'

    ticker = ForeignKeyField(Ticker, column_name='ticker', on_delete='CASCADE')


MODELS = (GroupBaseChart, GroupConfiguration, GroupMenu, GroupTicker)
