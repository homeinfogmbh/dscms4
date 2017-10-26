"""Quotes charts."""

from peewee import Model
from dscms4.orm.charts.common import Chart

__all__ = ['Quotes']


class Quotes(Model, Chart):
    """Chart for quotations."""

    class Meta:
        db_table = 'chart_quotes'

    @classmethod
    def from_dict(cls, dictionary):
        """Yields the chart."""
        yield super().from_dict(dictionary)
