"""New charts."""

from peewee import IntegerField, SmallIntegerField, BooleanField, CharField

from peeweeplus import JSONField

from dscms4 import dom
from dscms4.orm.charts.common import Chart

__all__ = ['News']


class News(Chart):
    """Chart to display news."""

    class Meta:
        table_name = 'chart_news'

    font_size_title = JSONField(
        SmallIntegerField, default=8, key='fontSizeTitle')
    title_color = JSONField(IntegerField, default=0x000000, key='titleColor')
    font_size_text = JSONField(SmallIntegerField, default=8, key='fontSizeText')
    text_color = JSONField(IntegerField, default=0x000000, key='textColor')
    ken_burns = JSONField(BooleanField, null=True, key='kenBurns')
    news_token = JSONField(CharField, 36, null=True, key='newsToken')

    def to_dom(self, brief=False):
        """Returns an XML DOM of this chart."""
        if brief:
            return super().to_dom(dom.BriefChart)

        xml = super().to_dom(dom.News)
        xml.font_size_title = self.font_size_title
        xml.title_color = self.title_color
        xml.font_size_text = self.font_size_text
        xml.text_color = self.text_color
        xml.ken_burns = self.ken_burns
        xml.news_token = self.news_token
        return xml
