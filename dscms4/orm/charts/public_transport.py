"""Local public transport charts."""

from peewee import Model
from dscms4.orm.charts.common import Chart

__all__ = ['PublicTransport']


class PublicTransport(Model, Chart):
    """Public transport chart."""

    class Meta:
        db_table = 'chart_public_transport'
