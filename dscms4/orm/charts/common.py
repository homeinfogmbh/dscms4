"""Common chart models."""

from contextlib import suppress
from datetime import datetime
from enum import Enum

from peewee import DoesNotExist, Model, ForeignKeyField, CharField, \
    TextField, DateTimeField, SmallIntegerField

from peeweeplus import EnumField

from dscms4.orm.common import DSCMS4Model, CustomerModel
from dscms4.orm.exceptions import OrphanedBaseChart
from dscms4.orm.schedule import Schedule


__all__ = [
    'DEFAULT_DURATION',
    'TransitionEffect',
    'BaseChart',
    'Chart']

DEFAULT_DURATION = 10


class TransitionEffect(Enum):
    """Effects available for chart transitions."""

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
    transition_effect = EnumField(TransitionEffect)

    @classmethod
    def add(cls, customer, title, description=None, duration=None,
            schedule=None, transition_effect=TransitionEffect.NONE):
        """Adds a new chart."""
        chart = cls()
        chart.customer = customer
        chart.title = title
        chart.description = description
        chart.duration = duration
        chart.created = datetime.now()
        chart.schedule = schedule
        chart.transition_effect = transition_effect
        chart.save()
        return chart

    @classmethod
    def from_dict(cls, customer, dictionary, schedule=None):
        """Creates a base chart from a dictionary
        for the respective customer.
        """
        return cls.add(
            customer,
            dictionary['title'],
            description=dictionary.get('description'),
            duration=dictionary.get('duration'),
            schedule=schedule,
            transition_effect=dictionary.get('description'))

    @property
    def active(self):
        """Determines whether the chart is considered active."""
        return self.schedule is None or self.schedule.active

    @property
    def chart(self):
        """Returns the mapped implementation of this chart."""
        from dscms4.orm.charts import CHARTS

        for _, cls in CHARTS.items():
            with suppress(DoesNotExist):
                return cls.get(cls.base_chart == self)

        raise OrphanedBaseChart(self)

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

    base_chart = ForeignKeyField(BaseChart, db_column='base_chart')

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new chart from the respective dictionary."""
        chart = cls()
        chart.base_chart = BaseChart.from_dict(dictionary['base_chart'])
        return chart

    def to_dict(self, cascade=False):
        """Converts the chart into a JSON compliant dictionary."""
        dictionary = super().to_dict()
        dictionary['base_chart'] = self.base_chart.id
        return dictionary
