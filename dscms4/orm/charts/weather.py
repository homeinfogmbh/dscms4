"""Weather chart."""

from peewee import Model
from dscms4.orm.charts.common import Chart

__all__ = ['Weather']


class Weather(Model, Chart):
    """Weather data."""

    class Meta:
        db_table = 'chart_weather'

    @classmethod
    def from_dict(cls, dictionary):
        """Yields the chart."""
        yield super().from_dict(dictionary)
