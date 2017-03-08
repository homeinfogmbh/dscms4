"""Menus"""

from peewee import ForeignKeyField, CharField

from .common import DSCMS4Model
from .charts import BaseChart

__all__ = [
    'Menu',
    'MenuItem',
    'ChartItem']


class Menu(DSCMS4Model):
    """A Menu item"""

    name = CharField(255)

    @property
    def members(self):
        """Yields the menu's members"""
        yield from self.submenus
        yield from self.charts


class MenuItem(DSCMS4Model):
    """Menus within menus"""

    class Meta:
        db_table = 'menu_member'

    menu = ForeignKeyField(Menu, db_column='menu', related_name='submenus')
    member = ForeignKeyField(
        Menu, db_column='member', related_name='parents')


class ChartItem(DSCMS4Model):
    """Charts within menus"""

    class Meta:
        db_table = 'chart_member'

    menu = ForeignKeyField(Menu, db_column='menu', related_name='charts')
    member = ForeignKeyField(
        BaseChart, db_column='member', related_name='menus')