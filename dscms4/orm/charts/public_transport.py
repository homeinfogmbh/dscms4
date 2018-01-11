"""Local public transport charts."""

from dscms4.orm.charts.common import Chart

__all__ = ['PublicTransport']


class PublicTransport(Chart):
    """Public transport chart."""

    class Meta:
        db_table = 'chart_public_transport'
