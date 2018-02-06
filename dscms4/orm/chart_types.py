"""Chart type settings for the respective customers."""

from peewee import CharField

from dscms4.orm.charts import CHARTS
from dscms4.orm.common import CustomerModel

__all__ = ['ChartType']


class ChartType(CustomerModel):
    """Represents a chart type this customer can use."""

    chart_type = CharField(255)

    @classmethod
    def add(cls, customer, chart_type):
        """Adds a chart type."""
        try:
            return cls.get(
                (cls.customer == customer) & (cls.chart_type == chart_type))
        except cls.DoesNotExist:
            record = cls()
            record.customer = customer
            record.chart_type = chart_type
            return record

    @property
    def chart_class(self):
        """Returns the respective chart type's class."""
        return CHARTS[self.chart_type]

    @chart_class.setter
    def chart_class(self, chart_class):
        """Sets the respective chart type by its class."""
        for name, cls in CHARTS.items():
            if cls == chart_class:
                self.chart_type = name
                break

    def to_dict(self):
        """Converts the record into a JSON compliant dictionary."""
        return self.chart_type
