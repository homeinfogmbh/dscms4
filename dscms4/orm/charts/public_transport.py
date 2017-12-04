"""Local public transport charts."""

from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model

__all__ = ['PublicTransport']


class PublicTransport(DSCMS4Model, Chart):
    """Public transport chart."""

    class Meta:
        db_table = 'chart_public_transport'
