"""Common chart models.

This module provides the base class "Chart"
for chart model implementation.
"""

from datetime import datetime
from enum import Enum
from uuid import uuid4

from peewee import ForeignKeyField, CharField, TextField, DateTimeField, \
    SmallIntegerField, BooleanField

from his.messages import MissingData
from peeweeplus import EnumField, UUID4Field

from dscms4 import dom
from dscms4.orm.common import DSCMS4Model, CustomerModel, RecordGroup

__all__ = ['BaseChart', 'Chart']


class Transitions(Enum):
    """Effects available for chart transition effects."""

    FADE_IN = 'fade-in'
    MOSAIK = 'mosaik'
    SLIDE_IN = 'slide-in'
    RANDOM = 'random'
    NONE = None


class ChartGroup(RecordGroup):
    """A Record group with a chart property."""

    @property
    def chart(self):
        """Reutns the chart record."""
        for record in self:
            if isinstance(record, Chart):
                return record


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
    log = BooleanField(default=False)
    _uuid = UUID4Field(column_name='uuid', null=True, default=None)

    @classmethod
    def from_dict(cls, customer, dictionary, *kwargs):
        """Creates the base chart from the provided dictionary."""
        record = super().from_dict(customer, dictionary, **kwargs)
        record.uuid = uuid4() if record.log else None
        return record

    @property
    def uuid(self):
        """Returns the UUID."""
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the UUID."""
        self._uuid = uuid

    @property
    def active(self):
        """Determines whether the chart is considered active."""
        now = datetime.now()
        return all((
            self.display_from is None or self.display_from > now,
            self.display_until is None or self.display_until < now))

    def patch(self, dictionary, **kwargs):
        """Patches the base chart."""
        record = super().patch(dictionary, **kwargs)
        record.uuid = uuid4() if record.log else None
        return record

    def to_dict(self, *args, **kwargs):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_dict(*args, **kwargs)
        dictionary['uuid'] = self.uuid
        return dictionary

    def to_dom(self):
        """Returns an XML DOM of the base chart."""
        xml = dom.BaseChart()
        xml.title = self.title
        xml.description = self.description
        xml.duration = self.duration
        xml.display_from = self.display_from
        xml.display_until = self.display_until
        xml.transition = self.transition.value
        xml.created = self.created
        xml.trashed = self.trashed
        xml.uuid = self.uuid.hex
        return xml


class Chart(DSCMS4Model):
    """Abstract basic chart."""

    base = ForeignKeyField(BaseChart, column_name='base', on_delete='CASCADE')

    @classmethod
    def from_dict(cls, customer, dictionary, **kwargs):
        """Creates a new chart from the respective dictionary."""
        try:
            base_dict = dictionary.pop('base')
        except KeyError:
            raise MissingData(key='base')

        base = BaseChart.from_dict(customer, base_dict)
        yield base
        chart = super().from_dict(dictionary, **kwargs)
        chart.base = base
        yield chart

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
        yield self.base.patch(dictionary.pop('base', {}))  # Generate new UUID.
        yield super().patch(dictionary, **kwargs)

    def to_dict(self, *args, brief=False, **kwargs):
        """Converts the chart into a JSON compliant dictionary."""
        if brief:
            dictionary = {'id': self.id}
        else:
            dictionary = super().to_dict(*args, **kwargs)

        if not brief:
            dictionary['base'] = self.base.to_dict(primary_key=False)

        dictionary['type'] = self.__class__.__name__
        return dictionary

    def to_dom(self, model):
        """Returns an XML DOM of this chart."""
        xml = model()
        xml.id = self.id
        xml.type = self.__class__.__name__

        if model is dom.BriefChart:
            return xml

        xml.base = self.base.to_dom()
        return xml

    def delete_instance(self):
        """Deletes the base chart and thus (CASCADE) this chart."""
        return self.base.delete_instance()
