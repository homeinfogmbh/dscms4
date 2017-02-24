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
        for menu_item in MenuItem.select().where(MenuItem.menu == self):
            yield menu_item.member

        for chart_item in ChartItem.select().where(ChartItem.menu == self):
            yield chart_item.member


class MenuItem(DSCMS4Model):
    """Menus within menus"""

    class Meta:
        db_table = 'menu_member'

    menu = ForeignKeyField(Menu, db_column='menu')
    member = ForeignKeyField(Menu, db_column='member')


class ChartItem(DSCMS4Model):
    """Charts within menus"""

    class Meta:
        db_table = 'chart_member'

    menu = ForeignKeyField(Menu, db_column='menu')
    member = ForeignKeyField(BaseChart, db_column='member')
