"""Presentation data"""

from peewee import ForeignKeyField, CharField, SmallIntegerField

from homeinfo.crm import Customer

from .common import DSCMS4Model
from .charts import BaseChart
from .company import Group, Building, RentalUnit

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


class _ChartAssignment(DSCMS4Model):
    """Abstract class for chart assignments"""

    chart = ForeignKeyField(BaseChart, db_column='chart')
    index = SmallIntegerField(null=True, default=None)
    duration = SmallIntegerField(null=True, default=None)


class GroupChart(_ChartAssignment):
    """Charts for the respective group"""

    class Meta:
        db_table = 'group_chart'

    group = ForeignKeyField(Group)


class BuildingChart(_ChartAssignment):
    """Charts for the respective building"""

    class Meta:
        db_table = 'building_chart'

    building = ForeignKeyField(Building)


class RentalUnitChart(_ChartAssignment):
    """Charts for the respective rental unit"""

    class Meta:
        db_table = 'rental_unit_chart'

    rental_unit = ForeignKeyField(RentalUnit)
