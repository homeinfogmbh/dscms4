"""Presentation data"""

from peewee import ForeignKeyField, CharField

from homeinfo.crm import Customer

from .common import DSCMS4Model
from .charts import BaseChart

__all__ = [
    'Menu',
    'MenuMember',
    'ChartMember',
    'Configuration']


class Menu(DSCMS4Model):
    """A Menu item"""

    name = CharField(255)

    @property
    def members(self):
        """Yields the menu's members"""
        for menu_member in MenuMember.select().where(MenuMember.menu == self):
            yield menu_member.member

        for chart_member in ChartMember.select().where(
                ChartMember.menu == self):
            yield chart_member.member


class MenuMember(DSCMS4Model):
    """Menus within menus"""

    class Meta:
        db_table = 'menu_member'

    menu = ForeignKeyField(Menu, db_column='menu')
    member = ForeignKeyField(Menu, db_column='member')


class ChartMember(DSCMS4Model):
    """Menus within menus"""

    class Meta:
        db_table = 'chart_member'

    menu = ForeignKeyField(Menu, db_column='menu')
    member = ForeignKeyField(BaseChart, db_column='member')


class Configuration(DSCMS4Model):
    """Customer configuration for charts"""

    customer = ForeignKeyField(Customer, db_column='customer')
    # TODO: Add configurations for all possible charts
