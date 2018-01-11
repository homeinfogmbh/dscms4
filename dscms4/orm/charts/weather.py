"""Weather chart."""

from dscms4.orm.charts.common import Chart

__all__ = ['Weather']


class Weather(Chart):
    """Weather data."""

    class Meta:
        db_table = 'chart_weather'
