"""Garbage collection chart."""

from peewee import Model
from dscms4.orm.charts.common import Chart

__all__ = ['GarbageCollection']


class GarbageCollection(Model, Chart):
    """Chart for garbage collection."""

    class Meta:
        db_table = 'chart_garbage_collection'
