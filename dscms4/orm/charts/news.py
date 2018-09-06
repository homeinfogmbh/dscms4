"""New charts."""

from peewee import IntegerField, SmallIntegerField, BooleanField, CharField

from dscms4 import dom
from dscms4.orm.charts.common import Chart

__all__ = ['News']


class News(Chart):
    """Chart to display news."""

    class Meta:
        table_name = 'chart_news'

    font_size_title = SmallIntegerField(default=8)
    title_color = IntegerField(default=0x000000)
    font_size_text = SmallIntegerField(default=8)
    text_color = IntegerField(default=0x000000)
    ken_burns = BooleanField(null=True)
    news_token = CharField(36, null=True)

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
