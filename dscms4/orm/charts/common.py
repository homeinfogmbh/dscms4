"""Common chart models."""

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


class BaseChart(Model, CustomerModel):
    """Common basic chart data model."""

    class Meta:
        db_table = 'base_chart'

    title = CharField(255)
    description = TextField(null=True, default=None)
    duration = SmallIntegerField(default=DEFAULT_DURATION)
    created = DateTimeField()
    schedule = ForeignKeyField(
        Schedule, db_column='schedule', null=True, default=None)
    transition = EnumField(Transitions)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a base chart from a dictionary
        for the respective customer.
        """
        chart = cls()
        chart.title = dictionary['title']
        chart.description = dictionary.get('description')
        chart.duration = dictionary.get('duration')
        chart.created = datetime.now()
        transition_ = dictionary.get('transition')

        for transition in Transitions:
            if transition.value == transition_:
                break
        else:
            transition = Transitions.NONE

        chart.transition = transition

        try:
            schedule = dictionary['schedule']
        except KeyError:
            schedule = None
        else:
            schedule = Schedule.from_dict(schedule)

        chart.schedule = schedule
        return chart

    @property
    def active(self):
        """Determines whether the chart is considered active."""
        return self.schedule is None or self.schedule.active

    def to_dict(self):
        """Returns a JSON compatible dictionary."""
        dictionary = super().to_dict()
        dictionary.update({
            'title': self.title,
            'description': self.description,
            'duration': self.duration,
            'created': self.created.isoformat(),
            'transition_effect': self.transition_effect.value})

        if self.schedule:
            dictionary['schedule'] = self.schedule.id
        else:
            dictionary['schedule'] = None

        return dictionary


class Chart(DSCMS4Model):
    """Abstract basic chart."""

    base = ForeignKeyField(BaseChart, db_column='base')

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new chart from the respective dictionary.

        This will NOT set the required customer.
        """
        chart = cls()
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

    def to_dict(self):
        """Converts the chart into a JSON compliant dictionary."""
        dictionary = super().to_dict()
        dictionary['base'] = self.base.id
        return dictionary

    def save(self):
        """Saves itself and its base chart."""
        Model.save(self)
        self.base.save()
