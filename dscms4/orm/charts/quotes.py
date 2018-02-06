"""Quotes charts."""

from peewee import IntegerField

from dscms4.orm.charts.common import Chart

__all__ = ['Quotes']


class Quotes(Chart):
    """Chart for quotations."""

    class Meta:
        table_name = 'chart_quotes'

    font_color = IntegerField(0x000000)
    background_color = IntegerField(0x000000)
