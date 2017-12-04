"""Weather chart."""

from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model

__all__ = ['Weather']


class Weather(DSCMS4Model, Chart):
    """Weather data."""

    class Meta:
        db_table = 'chart_weather'
