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
    'MODELS']


class _GroupContent(DSCMS4Model):
    """Common abstract content mapping."""

    group = ForeignKeyField(Group, column_name='group', on_delete='CASCADE')


class GroupBaseChart(_GroupContent):
    """Association of a base chart with a group."""

    class Meta:
        table_name = 'group_base_chart'

    base_chart = ForeignKeyField(
        BaseChart, column_name='base_chart', on_delete='CASCADE')


class GroupConfiguration(_GroupContent):
    """Association of a configuration with a group."""

    class Meta:
        table_name = 'group_configuration'

    configuration = ForeignKeyField(
        Configuration, column_name='configuration', on_delete='CASCADE')


class GroupMenu(_GroupContent):
    """Association of a menu with a group."""

    class Meta:
        table_name = 'group_menu'

    menu = ForeignKeyField(Menu, column_name='menu', on_delete='CASCADE')


MODELS = (GroupBaseChart, GroupConfiguration, GroupMenu)
