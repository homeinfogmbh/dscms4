"""New charts."""

from peewee import IntegerField, SmallIntegerField, BooleanField

from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model

__all__ = ['News']


DEFAULT_FONT_SIZE = 8
DEFAULT_COLOR = 0x000000


class News(DSCMS4Model, Chart):
    """Chart to display news."""

    class Meta:
        db_table = 'chart_news'

    font_size_title = SmallIntegerField(default=DEFAULT_FONT_SIZE)
    title_color = IntegerField(default=DEFAULT_COLOR)
    font_size_text = SmallIntegerField(default=DEFAULT_FONT_SIZE)
    text_color = IntegerField(default=DEFAULT_COLOR)
    ken_burns = BooleanField(null=True, default=None)
