"""Content assigned to groups."""

from peewee import DoesNotExist, Model, ForeignKeyField

from dscms4.orm.charts import BaseChart
from dscms4.orm.common import DSCMS4Model
from dscms4.orm.configuration import Configuration
from dscms4.orm.group import Group
from dscms4.orm.menu import Menu
from dscms4.orm.ticker import Ticker

__all__ = [
    'GroupBaseChart',
    'GroupConfiguration',
    'GroupMenu',
    'GroupTicker']


class GroupContent(DSCMS4Model):
    """Common abstract content mapping."""

    group = ForeignKeyField(Group, db_column='group')


class GroupBaseChart(Model, GroupContent):
    """Association of a base chart with a group."""

    class Meta:
        db_table = 'group_base_chart'

    base_chart = ForeignKeyField(BaseChart, db_column='base_chart')


class GroupConfiguration(Model, GroupContent):
    """Association of a configuration with a group."""

    class Meta:
        db_table = 'group_configuration'

    configuration = ForeignKeyField(Configuration, db_column='configuration')


class GroupMenu(Model, GroupContent):
    """Association of a menu with a group."""

    class Meta:
        db_table = 'group_menu'

    menu = ForeignKeyField(Menu, db_column='menu')


class GroupTicker(Model, GroupContent):
    """Association of a ticker with a group."""

    class Meta:
        db_table = 'group_ticker'

    ticker = ForeignKeyField(Ticker, db_column='ticker')
