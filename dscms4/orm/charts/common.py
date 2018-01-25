"""Common chart models.

This module provides the base class "Chart"
for chart model implementation.
"""

from datetime import datetime
from enum import Enum
from itertools import chain

from peewee import ForeignKeyField, CharField, TextField, DateTimeField, \
    SmallIntegerField, BooleanField

from peeweeplus import EnumField

from dscms4.orm.common import DSCMS4Model, CustomerModel


__all__ = ['BaseChart', 'Chart']

DEFAULT_DURATION = 10
ALLOW = ('base',)


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


class BaseChart(CustomerModel):
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

    def to_dict(self, id=True):
        """Returns a JSON-ish dictionary."""
        return super().to_dict(ignore=None if id else self.__class__.id)


class Chart(DSCMS4Model):
    """Abstract basic chart."""

    base = ForeignKeyField(BaseChart, db_column='base', on_delete='CASCADE')

    def __str__(self):
        """Generic string representation of the respective chart."""
        return '{}@{}'.format(self.id, self.__class__.__name__)

    @classmethod
    def from_dict(cls, customer, dictionary, allow=None, **kwargs):
        """Creates a new chart from the respective dictionary."""
        allow = ALLOW if allow is None else tuple(chain(allow, ALLOW))
        chart = super().from_dict(dictionary, allow=allow, **kwargs)
        chart.base = BaseChart.from_dict(dictionary['base'], customer=customer)
        return chart

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

    def patch(self, dictionary):
        """Pathes the chart with the provided dictionary."""
        base_dictionary = dictionary.get('base')

        if base_dictionary:
            yield self.base.patch(base_dictionary)

        yield super().patch(dictionary)

    def to_dict(self):
        """Converts the chart into a JSON compliant dictionary."""
        dictionary = super().to_dict()
        dictionary['base'] = self.base.to_dict(id=False)
        return dictionary

    def save(self):
        """Saves itself and its base chart."""
        self.base.save()
        super().save()

    def delete_instance(self):
        """Deletes this chart."""
        return self.base.delete_instance()
