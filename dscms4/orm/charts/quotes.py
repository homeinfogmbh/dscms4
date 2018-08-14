"""Quotes charts."""

from peewee import IntegerField

from peeweeplus import JSONField

from dscms4 import dom
from dscms4.orm.charts.common import Chart

__all__ = ['Quotes']


class Quotes(Chart):
    """Chart for quotations."""

    class Meta:
        table_name = 'chart_quotes'

    font_color = JSONField(IntegerField, 0x000000, key='fontColor')
    background_color = JSONField(IntegerField, 0x000000, key='backgroundColor')

    def to_dom(self, brief=False):
        """Returns an XML DOM of this chart."""
        if brief:
            return super().to_dom(dom.BriefChart)

        xml = super().to_dom(dom.Quotes)
        xml.font_color = self.font_color
        xml.background_color = self.background_color
        return xml
