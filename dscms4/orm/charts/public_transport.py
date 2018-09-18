"""Local public transport charts."""

from dscms4 import dom
from dscms4.orm.charts.common import Chart, RegisteredChart


__all__ = ['PublicTransport']


class PublicTransport(Chart, metaclass=RegisteredChart):
    """Public transport chart."""

    class Meta:
        table_name = 'chart_public_transport'

    def to_dom(self, brief=False):
        """Returns an XML DOM of this chart."""
        if brief:
            return super().to_dom(dom.BriefChart)

        return super().to_dom(dom.PublicTransport)
