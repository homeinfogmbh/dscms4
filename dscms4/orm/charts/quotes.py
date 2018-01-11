"""Quotes charts."""

from peewee import IntegerField

from dscms4.orm.charts.common import Chart

__all__ = ['Quotes']


DEFAULT_COLOR = 0x000000


class Quotes(Chart):
    """Chart for quotations."""

    class Meta:
        db_table = 'chart_quotes'

    font_color = IntegerField(DEFAULT_COLOR)
    background_color = IntegerField(DEFAULT_COLOR)
