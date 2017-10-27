"""Quotes charts."""

from peewee import Model, IntegerField

from dscms4.orm.charts.common import Chart

__all__ = ['Quotes']


DEFAULT_COLOR = 0x000000


class Quotes(Model, Chart):
    """Chart for quotations."""

    class Meta:
        db_table = 'chart_quotes'

    font_color = IntegerField(DEFAULT_COLOR)
    background_color = IntegerField(DEFAULT_COLOR)

    @classmethod
    def from_dict(cls, dictionary):
        """Yields the chart."""
        chart = super().from_dict(dictionary)
        chart.font_color = dictionary.get('font_color', DEFAULT_COLOR)
        chart.background_color = dictionary.get(
            'background_color', DEFAULT_COLOR)
        return chart
