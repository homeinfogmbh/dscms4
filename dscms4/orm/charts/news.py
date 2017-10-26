"""New charts."""

from peewee import Model
from dscms4.orm.charts.common import Chart

__all__ = ['News']


class News(Model, Chart):
    """Chart to display news."""

    class Meta:
        db_table = 'chart_news'

    localization = CharField(255, null=True, default=None)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new news chart from the
        provided JSON compliant dictionary.
        """
        chart = super().from_dict(dictionary)
        chart.localization = dictionary.get('localization')
        yield chart

    def to_dict(self):
        """Converts the chart record into a JSON compliant dictionary."""
        dictionary = super().to_dict()

        if self.localization is not None:
            dictionary['localization'] = self.localization

        return dictionary
