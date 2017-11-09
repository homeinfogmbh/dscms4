"""DSCMS4 WSGI handlers for charts."""

from peewee import DoesNotExist

from wsgilib import JSON

from dscms4.wsgi.common import DSCMS4Service
from dscms4.wsgi.messages import ChartDataIncomplete, ChartDataInvalid, \
    NoChartTypeSpecified, InvalidChartType, NoChartIdSpecified, \
    NoSuchChart, ChartAdded, ChartDeleted, ChartPatched, InvalidId
from dscms4.orm.charts import CHARTS
from dscms4.orm.exceptions import InvalidData, MissingData

__all__ = ['Chart']


def parse_chart_types(string, sep=','):
    """Parses the chart type names from the respective string."""

    return filter(None, map(lambda item: item.strip(), string.split(sep)))


class Chart(DSCMS4Service):
    """Manages charts."""

    NODE = 'dscms4'

    @property
    def chart_types(self):
        """Yields selected chart types."""
        try:
            chart_types = self.query['types']
        except KeyError:
            for _, chart_type in CHARTS.items():
                yield chart_type
        else:
            for chart_type in parse_chart_types(chart_types):
                try:
                    yield CHARTS[chart_type]
                except KeyError:
                    raise InvalidChartType() from None

    @property
    def chart_type(self):
        """Returns the selected chart type."""
        try:
            chart_type = self.query['type']
        except KeyError:
            raise NoChartTypeSpecified() from None

        try:
            return CHARTS[chart_type]
        except KeyError:
            raise InvalidChartType() from None

    @property
    def chart_id(self):
        """Returns the specified chart ID."""
        try:
            return int(self.resource)
        except TypeError:
            raise NoChartIdSpecified() from None
        except ValueError:
            raise InvalidId() from None

    @property
    def charts(self):
        """Lists the available charts."""
        for chart_type in self.chart_types:
            for chart in chart_type.select().where(
                    chart_type.customer == self.customer):
                yield chart

    @property
    def chart(self):
        """Returns the selected chart."""
        chart_type = self.chart_type

        try:
            return chart_type.get(
                (chart_type.id == self.chart_id) &
                (chart_type.customer == self.customer))
        except DoesNotExist:
            raise NoSuchChart() from None

    def get_chart_type(self, chart_dict):
        """Returns the chart type."""
        try:
            return self.chart_type
        except NoChartTypeSpecified:
            try:
                return CHARTS[chart_dict['type']]
            except KeyError:
                raise NoChartTypeSpecified() from None

    def get(self):
        """Lists charts or retrieves single chart."""
        if self.resource is None:
            return JSON([chart.to_dict() for chart in self.charts])

        return JSON(self.chart.to_dict())

    def post(self):
        """Adds new charts."""
        chart_dict = self.data.json
        chart_type = self.get_chart_type(chart_dict)

        try:
            chart = chart_type.from_dict(chart_dict)
        except MissingData as missing_data:
            raise ChartDataIncomplete(missing_data.missing) from None
        except InvalidData as invalid_data:
            raise ChartDataInvalid(invalid_data.invalid) from None
        else:
            return ChartAdded(id=chart.id)

    def delete(self):
        """Deletes the specified chart."""
        if self.resource is None:
            raise NoChartIdSpecified() from None

        chart_type = self.chart_type

        try:
            chart = chart_type.get(chart_type.id == self.chart_id)
        except DoesNotExist:
            raise NoSuchChart() from None
        else:
            chart.remove()
            return ChartDeleted()

    def patch(self):
        """Patches a chart."""
        self.chart.patch(self.data.json)
        return ChartPatched()
