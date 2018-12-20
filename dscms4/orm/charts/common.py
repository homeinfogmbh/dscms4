"""Common chart models.

This module provides the base class "Chart"
for chart model implementation.
"""
from collections import namedtuple
from datetime import datetime
from enum import Enum
from itertools import chain
from logging import getLogger
from uuid import uuid4

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import ModelBase
from peewee import SmallIntegerField
from peewee import TextField
from peewee import UUIDField

from his.messages import MissingData
from peeweeplus import EnumField    # pylint: disable=E0401

from dscms4 import dom  # pylint: disable=E0611
from dscms4.exceptions import OrphanedBaseChart, AmbiguousBaseChart
from dscms4.orm.common import DSCMS4Model, CustomerModel


__all__ = ['BaseChart', 'Chart']


LOGGER = getLogger(__file__)
CheckResult = namedtuple('CheckResult', ('orphans', 'ambiguous'))


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

    def resolve_refs(self, model, records, json_objects, *,
                     record_identifier=lambda record: record.id,
                     json_identifier=lambda json: json.get('id')):
        """Resolves chart-referencing records for
        JSON deserialization and patching.
        """
        records = {record_identifier(record): record for record in records}
        json_objects = {json_identifier(json): json for json in json_objects}
        processed = set()

        for ident, record in records.items():
            processed.add(ident)

            try:
                json = json_objects[ident]
            except KeyError:
                self.delete(record)
            else:
                record.patch(json)
                self.add(record)

        for ident, json in json_objects.items():
            if ident not in processed:
                record = model.from_json(json, self.chart)
                self.add(record)

        return self

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


class ChartMode(Enum):
    """JSON serialization modes."""

    FULL = 'full'
    BRIEF = 'brief'
    ANON = 'anon'


class BaseChart(CustomerModel):
    """Common basic chart data model."""

    class Meta:     # pylint: disable=C0111,R0903
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
    uuid = UUIDField(null=True)

    @classmethod
    def from_json(cls, json, skip=None, **kwargs):
        """Creates a base chart from a JSON-ish dictionary."""
        skip_default = ('uuid',)
        skip = tuple(chain(skip_default, skip)) if skip else skip_default
        record = super().from_json(json, skip=skip, **kwargs)
        record.uuid = uuid4() if record.log else None
        return record

    @classmethod
    def check(cls, verbose=False):
        """Checks base charts."""
        orphans = set()
        ambiguous = set()

        for base_chart in cls:
            try:
                chart = base_chart.chart
            except OrphanedBaseChart as orphaned_base_chart:
                orphans.add(base_chart)

                if verbose:
                    LOGGER.error(orphaned_base_chart)
            except AmbiguousBaseChart as ambiguous_base_chart:
                ambiguous.add(base_chart)

                if verbose:
                    LOGGER.error(ambiguous_base_chart)
            else:
                if verbose:
                    LOGGER.info('%s ↔ %s', base_chart, chart)

        return CheckResult(frozenset(orphans), frozenset(ambiguous))

    @property
    def active(self):
        """Determines whether the chart is considered active."""
        now = datetime.now()
        return all((
            self.display_from is None or self.display_from > now,
            self.display_until is None or self.display_until < now))

    @property
    def charts(self):
        """Yields all charts that associate this base chart."""
        for model in Chart.types.values():
            for record in model.select().where(model.base == self):
                yield record

    @property
    def chart(self):
        """Returns the mapped implementation of this base chart."""
        try:
            match, *superfluous = self.charts
        except ValueError:
            raise OrphanedBaseChart(self)

        if superfluous:
            charts = frozenset([match] + superfluous)
            raise AmbiguousBaseChart(self, charts)

        return match

    def patch_json(self, json, **kwargs):
        """Patches the base chart."""
        super().patch_json(json, **kwargs)
        self.uuid = uuid4() if self.log else None

    def to_json(self, brief=False, **kwargs):
        """Returns a JSON-ish dictionary."""
        if brief:
            return {'title': self.title}

        return super().to_json(**kwargs)

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


class MetaChart(ModelBase):
    """Metaclass for charts."""

    _implementations = {}

    def __init__(cls, *args, **kwargs):
        """Registers the different chart types."""
        super().__init__(*args, **kwargs)
        cls._implementations[cls.__name__] = cls

    @property
    def types(cls):
        """Yields chart types."""
        return {
            name: class_ for name, class_ in cls._implementations.items()
            if class_ is not Chart}


class Chart(DSCMS4Model, metaclass=MetaChart):
    """Abstract basic chart."""

    base = ForeignKeyField(BaseChart, column_name='base', on_delete='CASCADE')

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

    def to_json(self, mode=ChartMode.FULL, **kwargs):
        """Returns a JSON-ish dictionary."""
        if mode == ChartMode.FULL:
            json = super().to_json(**kwargs)
            json['base'] = self.base.to_json(autofields=False)
        elif mode == ChartMode.BRIEF:
            json = {'id': self.id}
        elif mode == ChartMode.ANON:
            json = super().to_json(skip=('id',), **kwargs)
            json['base'] = self.base.to_json(autofields=False)
            return json

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
