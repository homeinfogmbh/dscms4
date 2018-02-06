"""New charts."""

from peewee import IntegerField, SmallIntegerField, BooleanField

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
