"""Common chart models."""

from contextlib import suppress
from datetime import datetime
from enum import Enum

from peewee import Model, ForeignKeyField, CharField, TextField, \
    DateTimeField, SmallIntegerField

from peeweeplus import EnumField

from dscms4.orm.common import DSCMS4Model, CustomerModel
from dscms4.orm.schedule import Schedule


__all__ = ['BaseChart', 'Chart']

DEFAULT_DURATION = 10


class Transitions(Enum):
    """Effects available for chart transition effects."""

    FADE_IN = 'fade-in'
    MOSAIK = 'mosaik'
    SLIDE_IN = 'slide-in'
    RANDOM = 'random'
    NONE = None

    @classmethod
    def by_value(cls, value):
        """Returns the appropriate enumeration for the provided value."""
        for transition in cls:
            if transition.value == value:
                return transition

        raise ValueError('No such transition.')


class BaseChart(Model, CustomerModel):
    """Common basic chart data model."""

    class Meta:
        db_table = 'base_chart'

    title = CharField(255)
    description = TextField(null=True, default=None)
    duration = SmallIntegerField(default=DEFAULT_DURATION)
    display_from = DateTimeField(null=True, default=None)
    display_until = DateTimeField(null=True, default=None)
    transition = EnumField(Transitions)
    created = DateTimeField(default=datetime.now)

    @property
    def active(self):
        """Determines whether the chart is considered active."""
        now = datetime.now()

        if self.display_from is not None:
            if self.display_from > now:
                return False

        if self.display_until is not None:
            if self.display_until < now:
                return False

        return True


class Chart(DSCMS4Model):
    """Abstract basic chart."""

    base = ForeignKeyField(BaseChart, db_column='base')

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new chart from the respective dictionary.

        This will NOT set the required customer.
        """
        chart = super().from_dict(dictionary)
        chart.base = BaseChart.from_dict(dictionary['base'])
        return chart

    @property
    def customer(self):
        """Returns the base chart's customer."""
        return self.base.customer

    @customer.setter
    def customer(self, customer):
        """Sets the base chart's customer."""
        self.base.customer = customer

    def patch(self, dictionary):
        """Pathes the chart with the provided dictionary."""
        base_dictionary = dictionary.get('base')

        if base_dictionary:
            yield self.base.patch(base_dictionary)

        yield super().patch(dictionary)

    def to_dict(self):
        """Converts the chart into a JSON compliant dictionary."""
        dictionary = super().to_dict()
        dictionary['base'] = self.base.id
        return dictionary

    def save(self):
        """Saves itself and its base chart."""
        Model.save(self)
        self.base.save()
