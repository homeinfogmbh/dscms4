"""DSCMS4 WSGI handlers"""

from peewee import DoesNotExist

from his.api.messages import InvalidId
from wsgilib import JSON

from .common import AuthorizedJSONService
from .messages import ChartDataIncomplete, ChartDataInvalid, \
    NoChartTypeSpecified, InvalidChartType, NoChartIdSpecified, \
    NoSuchChart, ChartAdded, ChartDeleted
from ..orm.charts import CHARTS
from ..orm.exceptions import InvalidData, MissingData


class Charts(AuthorizedJSONService):
    """Manages charts"""

    NODE = 'dscms4'

    @property
    def chart_types(self):
        """Yields selected chart types"""
        chart_types = self.query.get('types')

        if chart_types is not None:
            for chart_type in chart_types.split():
                chart_type = chart_type.strip()

                if chart_type:
                    try:
                        yield CHARTS[chart_type]
                    except KeyError:
                        raise InvalidChartType() from None
        else:
            for chart_type in CHARTS:
                yield CHARTS[chart_type]

    @property
    def chart_type(self):
        """Returns the selected chart type"""
        try:
            chart_type = self.query['type']
        except KeyError:
            raise NoChartTypeSpecified() from None
        else:
            try:
                return CHARTS[chart_type]
            except KeyError:
                raise InvalidChartType() from None

    @property
    def chart_id(self):
        """Returns the specified chart ID"""
        try:
            return int(self.resource)
        except TypeError:
            raise NoChartIdSpecified() from None
        except ValueError:
            raise InvalidId() from None

    @property
    def charts(self):
        """Lists the available charts"""
        for chart_type in self.chart_types:
            for chart in chart_type.select().where(
                    chart_type.customer == self.customer):
                yield chart

    @property
    def chart(self):
        """Returns the selected chart"""
        chart_type = self.chart_type

        try:
            return chart_type.get(
                (chart_type.id == self.chart_id) &
                (chart_type.customer == self.customer))
        except DoesNotExist:
            raise NoSuchChart() from None

    def get_chart_type(self, chart_dict):
        """Returns the chart type"""
        try:
            return self.chart_type
        except NoChartTypeSpecified:
            try:
                return CHARTS[chart_dict['type']]
            except KeyError:
                raise NoChartTypeSpecified()

    def get(self):
        """Lists charts or retrieves single chart"""
        if self.resource is None:
            return JSON([chart.to_dict() for chart in self.charts])
        else:
            return JSON(self.chart.to_dict())

    def post(self):
        """Adds new charts"""
        chart_dict = self.json
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
        """Deletes the specified chart"""
        if self.resource is None:
            raise NoChartIdSpecified() from None
        else:
            chart_type = self.chart_type

            try:
                chart = chart_type.get(chart_type.id == self.chart_id)
            except DoesNotExist:
                raise NoSuchChart() from None
            else:
                chart.remove()
                return ChartDeleted()

    def patch(self):
        """Patches a chart"""
        raise NotImplementedError()
