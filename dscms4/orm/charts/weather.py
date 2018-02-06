"""Weather chart."""

from dscms4.orm.charts.common import Chart

__all__ = ['Weather']


class Weather(Chart):
    """Weather data."""

    class Meta:
        table_name = 'chart_weather'
