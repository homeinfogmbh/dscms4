"""Group contents."""

from peewee import DoesNotExist, Model, ForeignKeyField

from ..charts import BaseChart
from ..common import DSCMS4Model
from ..configuration import Configuration
from ..group import Group
from ..menu import Menu

__all__ = ['GroupBaseChart', 'GroupConfiguration', 'GroupMenu', 'GroupTicker']


class GroupContent(DSCMS4Model):
    """Common abstract content mapping."""

    group = ForeignKeyField(Group, db_column='group')
    content = None

    @classmethod
    def _add(cls, group, content):
        """Adds a new association of content with a group."""
        mapping = cls()
        mapping.group = group
        mapping.content = content

    @classmethod
    def add(cls, group, content):
        """Adds a new association of content with
        a group iff it does not yet exist.
        """
        try:
            return cls.get((cls.group == group) & (cls.content == content))
        except DoesNotExist:
            return cls._add(group, content)


class GroupBaseChart(Model, GroupContent):
    """Association of a base chart with a group."""

    class Meta:
        db_table = 'group_base_chart'

    content = ForeignKeyField(BaseChart, db_column='base_chart')


class GroupConfiguration(Model, GroupContent):
    """Association of a configuration with a group."""

    class Meta:
        db_table = 'group_configuration'

    content = ForeignKeyField(Configuration, db_column='configuration')


class GroupMenu(Model, GroupContent):
    """Association of a menu with a group."""

    class Meta:
        db_table = 'group_menu'

    content = ForeignKeyField(Menu, db_column='menu')


class GroupTicker(Model, GroupContent):
    """Association of a ticker with a group."""

    class Meta:
        db_table = 'group_ticker'

    content = ForeignKeyField(Ticker, db_column='ticker')
