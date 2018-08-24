"""Common chart models.

This module provides the base class "Chart"
for chart model implementation.
"""
from collections import namedtuple
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


class Transaction(namedtuple('Transaction', ('chart', 'related'))):
    """Stores chart and related records."""

    __slots__ = ()

    def __new__(cls, chart):
        """Creates a new transaction."""
        return super().__new__(cls, chart, [])

    def add(self, record):
        """Adds the record as to be added."""
        self.related.append((True, record))

    def delete(self, record):
        """Adds the record as to be deleted."""
        self.related.append((False, record))

    def commit(self):
        """Saves the base chart, chart and
        related record in preserved order.
        """
        self.chart.base.save()
        self.chart.save()

        for save, record in self.related:
            if save:
                record.save()
            else:
                record.delete_instance()


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
        """Creates a base chart from a JSON-ish dictionary."""
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
        super().patch_json(json, **kwargs)
        self.uuid = uuid4() if self.log else None

    def to_json(self, *args, **kwargs):
        """Returns a JSON-ish dictionary."""
        json = super().to_json(*args, **kwargs)

        if self.uuid:
            json['uuid'] = self.uuid.hex

        return json

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
        """Creates a chart from a JSON-ish dictionary."""
        try:
            base_dict = json.pop('base')
        except KeyError:
            raise MissingData(key='base')

        chart = super().from_json(json, **kwargs)
        chart.base = BaseChart.from_json(base_dict)
        return Transaction(chart)

    def patch_json(self, json, **kwargs):
        """Pathes the chart with the provided dictionary."""
        self.base.patch_json(json.pop('base', {}))  # Generate new UUID.
        super().patch_json(json, **kwargs)
        return Transaction(self)

    def to_json(self, brief=False, **kwargs):
        """Returns a JSON-ish dictionary."""
        if brief:
            json = {'id': self.id}
        else:
            json = super().to_json(**kwargs)

        if not brief:
            json['base'] = self.base.to_json(autofields=False)

        json['type'] = type(self).__name__
        return json

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
