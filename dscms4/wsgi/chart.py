"""DSCMS4 WSGI handlers"""

from .common import AuthorizedJSONService
from ..orm.charts import MODELS as CHARTS


class Charts(AuthorizedJSONService):
    """Manages charts"""

    CHARTS = {chart.__class__.__name__: chart for chart in CHARTS}

    @property
    def chart_types(self):
        """Yields selected chart types"""
        chart_types = self.query.get('types')

        if chart_types is not None:
            for chart_type in chart_types.split():
                chart_type = chart_type.strip()

                if chart_type:
                    try:
                        yield self.CHARTS[chart_type.lower()]
                    except KeyError:
                        raise InvalidChartType() from None
        else:
            for chart_type in self.CHARTS:
                yield self.CHARTS[chart_type]

    @property
    def chart_type(self):
        """Returns the selected chart type"""
        try:
            chart_type = self.query['type']
        except KeyError:
            raise NoChartTypeSpecified() from None
        else:
            try:
                return self.CHARTS[chart_type.lower()]
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

    def get(self):
        """Lists charts or retrieves single chart"""
        if self.resource is None:
            return JSON([chart.to_dict() for chart in self.charts])
        else:
            return JSON(self.chart.to_dict())

    def post(self):
        """Adds new charts"""
        try:
            chart = self.chart_type.from_dict(self.json)
        except MissingData:
            pass
        except InvalidData:
            pass
        else:
            return ChartAdded(id=chart.id)
