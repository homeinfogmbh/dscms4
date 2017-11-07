"""New charts."""

from peewee import Model, IntegerField, SmallIntegerField, BooleanField

from dscms4.orm.charts.common import Chart

__all__ = ['News']


DEFAULT_FONT_SIZE = 8
DEFAULT_COLOR = 0x000000


class News(Model, Chart):
    """Chart to display news."""

    class Meta:
        db_table = 'chart_news'

    font_size_title = SmallIntegerField(default=DEFAULT_FONT_SIZE)
    title_color = IntegerField(default=DEFAULT_COLOR)
    font_size_text = SmallIntegerField(default=DEFAULT_FONT_SIZE)
    text_color = IntegerField(default=DEFAULT_COLOR)
    ken_burns = BooleanField(null=True, default=None)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new news chart from the
        provided JSON compliant dictionary.
        """
        chart = super().from_dict(dictionary)
        chart.font_size_title = dictionary.get(
            'font_size_title', DEFAULT_FONT_SIZE)
        chart.title_color = dictionary.get('title_color', DEFAULT_COLOR)
        chart.font_size_text = dictionary.get(
            'font_size_text', DEFAULT_FONT_SIZE)
        chart.text_color = dictionary.get('text_color', DEFAULT_COLOR)
        chart.ken_burns = dictionary.get('ken_burns')
        return chart

    @property
    def dictionary(self):
        """Converts the chart record into a JSON compliant dictionary."""
        return {'localization': self.localization}
