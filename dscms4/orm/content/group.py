"""Content assigned to groups."""

from peewee import ForeignKeyField, IntegerField

from dscms4.orm.charts import ChartMode, BaseChart
from dscms4.orm.common import DSCMS4Model
from dscms4.orm.configuration import Configuration
from dscms4.orm.group import Group
from dscms4.orm.menu import Menu


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
    index = IntegerField(default=0)

    @property
    def chart(self):
        """Returns the respective chart."""
        return self.base_chart.chart

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {
            'id': self.id,
            'chart': self.chart.to_json(mode=ChartMode.BRIEF),
            'index': self.index}


class GroupConfiguration(_GroupContent):
    """Association of a configuration with a group."""

    class Meta:
        table_name = 'group_configuration'

    configuration = ForeignKeyField(
        Configuration, column_name='configuration', on_delete='CASCADE')

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {'id': self.id, 'configuration': self.configuration_id}


class GroupMenu(_GroupContent):
    """Association of a menu with a group."""

    class Meta:
        table_name = 'group_menu'

    menu = ForeignKeyField(Menu, column_name='menu', on_delete='CASCADE')

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {'id': self.id, 'menu': self.menu_id}


MODELS = (GroupBaseChart, GroupConfiguration, GroupMenu)
