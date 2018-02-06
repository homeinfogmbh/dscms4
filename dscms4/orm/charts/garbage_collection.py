"""Garbage collection chart."""

from dscms4.orm.charts.common import Chart

__all__ = ['GarbageCollection']


class GarbageCollection(Chart):
    """Chart for garbage collection."""

    class Meta:
        table_name = 'chart_garbage_collection'
