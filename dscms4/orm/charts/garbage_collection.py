"""Garbage collection chart."""

from dscms4 import dom
from dscms4.orm.charts.common import Chart, RegisteredChart


__all__ = ['GarbageCollection']


class GarbageCollection(Chart, metaclass=RegisteredChart):
    """Chart for garbage collection."""

    class Meta:
        table_name = 'chart_garbage_collection'

    def to_dom(self, brief=False):
        """Returns an XML DOM of this chart."""
        if brief:
            return super().to_dom(dom.BriefChart)

        return super().to_dom(dom.GarbageCollection)
