"""Garbage collection chart."""

from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model

__all__ = ['GarbageCollection']


class GarbageCollection(DSCMS4Model, Chart):
    """Chart for garbage collection."""

    class Meta:
        db_table = 'chart_garbage_collection'
