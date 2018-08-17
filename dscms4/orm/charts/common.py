"""Common chart models.

This module provides the base class "Chart"
for chart model implementation.
"""
from datetime import datetime
from enum import Enum
from itertools import chain
from uuid import uuid4

from peewee import CharField, TextField, DateTimeField, SmallIntegerField, \
    BooleanField, UUIDField

from his.messages import MissingData
from peeweeplus import EnumField

from dscms4 import dom
from dscms4.orm.common import RelatedKeyField, CustomerModel, RelatedModel


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
    log = BooleanField(default=False)
    uuid = UUIDField(column_name='uuid', null=True)

    @classmethod
    def from_json(cls, json, skip=None, **kwargs):
        """Creates the base chart from the provided dictionary."""
        skip_default = ('uuid',)
        skip = tuple(chain(skip_default, skip)) if skip else skip_default
        record = super().from_json(json, skip=skip, **kwargs)
        record.uuid = uuid4() if record.log else None
        return record

    @property
    def active(self):
        """Determines whether the chart is considered active."""
        now = datetime.now()
        return all((
            self.display_from is None or self.display_from > now,
            self.display_until is None or self.display_until < now))

    def patch_json(self, json, **kwargs):
        """Patches the base chart."""
        record = super().patch_json(json, **kwargs)
        record.uuid = uuid4() if record.log else None

    def to_json(self, *args, **kwargs):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_json(*args, **kwargs)

        if self.uuid:
            dictionary['uuid'] = self.uuid.hex

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

        if self.uuid:
            xml.uuid = self.uuid.hex

        return xml


class Chart(RelatedModel):
    """Abstract basic chart."""

    base = RelatedKeyField(BaseChart, column_name='base', on_delete='CASCADE')

    @classmethod
    def from_json(cls, json, **kwargs):
        """Creates a new chart from the respective dictionary."""
        try:
            base_dict = json.pop('base')
        except KeyError:
            raise MissingData(key='base')

        base = BaseChart.from_json(base_dict)
        yield base
        chart = super().from_json(json, **kwargs)
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

    def patch_json(self, json, **kwargs):
        """Pathes the chart with the provided dictionary."""
        self.base.patch(json.pop('base', {}))  # Generate new UUID.
        yield self.base
        super().patch(json, **kwargs)
        yield self

    def to_json(self, brief=False, **kwargs):
        """Converts the chart into a JSON compliant dictionary."""
        if brief:
            dictionary = {'id': self.id}
        else:
            dictionary = super().to_json(**kwargs)

        if not brief:
            dictionary['base'] = self.base.to_json(autofields=False)

        dictionary['type'] = type(self).__name__
        return dictionary

    def to_dom(self, model):
        """Returns an XML DOM of this chart."""
        xml = model()
        xml.id = self.id
        xml.type = type(self).__name__

        if model is dom.BriefChart:
            return xml

        xml.base = self.base.to_dom()
        return xml

    def delete_instance(self):
        """Deletes the base chart and thus (CASCADE) this chart."""
        return self.base.delete_instance()
