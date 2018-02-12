"""Common chart models.

This module provides the base class "Chart"
for chart model implementation.
"""

from datetime import datetime
from enum import Enum

from peewee import ForeignKeyField, CharField, TextField, DateTimeField, \
    SmallIntegerField, BooleanField

from his.messages import MissingData
from peeweeplus import EnumField

from dscms4.orm.common import DSCMS4Model, CustomerModel

__all__ = ['BaseChart', 'Chart']


class Transitions(Enum):
    """Effects available for chart transition effects."""

    FADE_IN = 'fade-in'
    MOSAIK = 'mosaik'
    SLIDE_IN = 'slide-in'
    RANDOM = 'random'
    NONE = None


class BaseChart(CustomerModel):
    """Common basic chart data model."""

    class Meta:
        table_name = 'base_chart'

    title = CharField(255)
    description = TextField(null=True)
    duration = SmallIntegerField(default=10)
    display_from = DateTimeField(null=True)
    display_until = DateTimeField(null=True)
    transition = EnumField(Transitions)
    created = DateTimeField(default=datetime.now)
    trashed = BooleanField(default=False)

    @property
    def active(self):
        """Determines whether the chart is considered active."""
        now = datetime.now()

        if self.display_from is not None and self.display_from > now:
            return False

        if self.display_until is not None and self.display_until < now:
            return False

        return True


class Chart(DSCMS4Model):
    """Abstract basic chart."""

    base = ForeignKeyField(BaseChart, column_name='base', on_delete='CASCADE')

    def __str__(self):
        """Generic string representation of the respective chart."""
        return '{}@{}'.format(self.id, self.__class__.__name__)

    @classmethod
    def from_dict(cls, customer, dictionary, **kwargs):
        """Creates a new chart from the respective dictionary."""
        try:
            base_dict = dictionary.pop('base')
        except KeyError:
            raise MissingData(key='base')

        chart = super().from_dict(dictionary, **kwargs)
        chart.base = BaseChart.from_dict(customer, base_dict)
        return chart

    @classmethod
    def by_customer(cls, customer):
        """Yields charts by customer."""
        return cls.select().join(BaseChart).where(
            BaseChart.customer == customer)

    @classmethod
    def by_id(cls, ident, customer=None):
        """Returns a single chart by its ID."""
        if customer is None:
            return cls.get(cls.id == ident)

        return cls.select().join(BaseChart).where(
            (cls.id == ident) & (BaseChart.customer == customer)).get()


    @property
    def customer(self):
        """Returns the base chart's customer."""
        return self.base.customer

    @customer.setter
    def customer(self, customer):
        """Sets the base chart's customer."""
        self.base.customer = customer

    @property
    def trashed(self):
        """Determines whether this chart is considered trashed."""
        return self.base.trashed

    @property
    def active(self):
        """Determines whether the chart is considered active."""
        return self.base.active

    def patch(self, dictionary, **kwargs):
        """Pathes the chart with the provided dictionary."""
        try:
            base = dictionary.pop('base')
        except KeyError:
            pass
        else:
            self.base.patch(base)

        return super().patch(dictionary, **kwargs)

    def to_dict(self, *args, base_chart=True, type_=True, **kwargs):
        """Converts the chart into a JSON compliant dictionary."""
        dictionary = super().to_dict(*args, **kwargs)

        if base_chart:
            dictionary['base'] = self.base.to_dict(primary_key=False)

        if type_:
            dictionary['type'] = self.__class__.__name__

        return dictionary

    def save(self, base=True):
        """Saves itself and its base chart."""
        if base:
            base_id = self.base.save()

        ident = super().save()
        return (ident, base_id)

    def delete_instance(self):
        """Deletes the base chart and thus (CASCADE) this chart."""
        return self.base.delete_instance()
