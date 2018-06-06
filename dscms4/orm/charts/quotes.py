"""Quotes charts."""

from peewee import IntegerField

from dscms4 import dom
from dscms4.orm.charts.common import Chart

__all__ = ['Quotes']


class Quotes(Chart):
    """Chart for quotations."""

    class Meta:
        table_name = 'chart_quotes'

    font_color = IntegerField(0x000000)
    background_color = IntegerField(0x000000)

    def to_dom(self):
        """Returns an XML DOM of this chart."""
        xml = super().to_dom(dom.Quotes)
        xml.font_color = self.font_color
        xml.background_color = self.background_color
        return xml
