"""Chart type settings for the respective customers."""

from peewee import CharField

from dscms4.orm.charts import Chart
from dscms4.orm.common import CustomerModel


__all__ = ['ChartType', 'MODELS']


class ChartType(CustomerModel):
    """Represents a chart type this customer can use."""

    chart_type = CharField(255)

    @property
    def chart_class(self):
        """Returns the respective chart type's class."""
        return Chart.types[self.chart_type]

    @chart_class.setter
    def chart_class(self, chart_class):
        """Sets the respective chart type by its class."""
        for name, cls in Chart.types.items():
            if cls == chart_class:
                self.chart_type = name
                break


MODELS = (ChartType,)
