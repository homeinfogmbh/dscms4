"""Aggregated presentation data"""

from peewee import ForeignKeyField, SmallIntegerField

from .common import DSCMS4Model
from .charts import BaseChart
from .company import Group, Building, RentalUnit


class _ChartAssignment(DSCMS4Model):
    """Abstract class for chart assignments"""

    chart = ForeignKeyField(BaseChart, db_column='chart')
    index = SmallIntegerField(null=True, default=None)
    duration = SmallIntegerField(null=True, default=None)

    @classmethod
    def add(cls, chart, index=None, duration=None):
        """Adds a new group chart mapping"""
        chart_assignment = cls()
        chart_assignment.chart = chart
        chart_assignment.index = index
        chart_assignment.duration = duration
        # Do not invoke save() because this Model is abstract!
        return chart_assignment


class GroupChart(_ChartAssignment):
    """Charts for the respective group"""

    class Meta:
        db_table = 'group_chart'

    group = ForeignKeyField(Group)

    @classmethod
    def add(cls, group, chart, index=None, duration=None):
        """Adds a new group chart mapping"""
        group_chart = super().add(chart, index=index, duration=duration)
        group_chart.group = group
        group_chart.save()
        return group_chart


class BuildingChart(_ChartAssignment):
    """Charts for the respective building"""

    class Meta:
        db_table = 'building_chart'

    building = ForeignKeyField(Building)

    @classmethod
    def add(cls, building, chart, index=None, duration=None):
        """Adds a new group chart mapping"""
        building_chart = super().add(chart, index=index, duration=duration)
        building_chart.building = building
        building_chart.save()
        return building_chart


class RentalUnitChart(_ChartAssignment):
    """Charts for the respective rental unit"""

    class Meta:
        db_table = 'rental_unit_chart'

    rental_unit = ForeignKeyField(RentalUnit)

    @classmethod
    def add(cls, rental_unit, chart, index=None, duration=None):
        """Adds a new group chart mapping"""
        rental_unit_chart = super().add(chart, index=index, duration=duration)
        rental_unit_chart.rental_unit = rental_unit
        rental_unit_chart.save()
        return rental_unit_chart
