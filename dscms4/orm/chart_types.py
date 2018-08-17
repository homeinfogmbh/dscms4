"""Chart type settings for the respective customers."""

from flask import has_request_context
from peewee import CharField

from his import CUSTOMER

from dscms4.config import LOGGER
from dscms4.orm.charts import CHARTS
from dscms4.orm.common import CustomerModel

__all__ = ['ChartType', 'MODELS']


class ChartType(CustomerModel):
    """Represents a chart type this customer can use."""

    chart_type = CharField(255)

    @classmethod
    def add(cls, chart_type, customer=None):
        """Adds a chart type."""
        if customer is not None:
            LOGGER.warning('Explicitely set customer to: %s.', customer)
        elif has_request_context():
            customer = CUSTOMER.id
        else:
            raise ValueError('No customer specified.')

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


MODELS = (ChartType,)
