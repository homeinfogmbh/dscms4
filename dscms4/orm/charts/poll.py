"""Chart for polls."""

from enum import Enum

from peewee import CharField, ForeignKeyField, IntegerField, TextField

from peeweeplus import EnumField

from dscms4 import dom
from dscms4.orm.charts.common import ChartMode, Chart
from dscms4.orm.common import UNCHANGED, DSCMS4Model


__all__ = ['PollMode', 'Poll', 'Option']


class PollMode(Enum):
    """Available poll modes."""

    SINGLE_CHOICE = 'single choice'
    MULTIPLE_CHOICE = 'multiple choice'


class Poll(Chart):
    """Chart to display a poll."""

    class Meta:
        table_name = 'chart_poll'

    text = TextField()
    mode = EnumField(PollMode)

    @classmethod
    def from_json(cls, json, **kwargs):
        """Creates a new poll from JSON."""
        options = json.pop('options', ())
        transaction = super().from_json(json, **kwargs)

        for option in options:
            option = Option.from_json(option, transaction.chart)
            transaction.add(option)

        return transaction

    @property
    def options(self):
        """Returns sorted options."""
        return Option.select().where(Option.poll == self).order_by(
            Option.index)

    def patch_json(self, json, **kwargs):
        """Patches the respective chart."""
        options = json.pop('options', UNCHANGED) or ()
        transaction = super().patch_json(json, **kwargs)

        if options is UNCHANGED:
            return transaction

        return transaction.resolve_refs(
            Option, self.options, options,
            record_identifier=lambda record: record.text,
            json_identifier=lambda obj: obj.get('text'))

    def to_json(self, mode=ChartMode.FULL, **kwargs):
        """Returns the dictionary representation of this chart's fields."""
        json = super().to_json(mode=mode, **kwargs)

        if mode == ChartMode.FULL:
            json['options'] = [
                option.to_json(fk_fields=False, autofields=True)
                for option in self.options.order_by(Option.index)]

        return json

    def to_dom(self, brief=False):
        """Returns an XML DOM of this chart."""
        if brief:
            return super().to_dom(dom.BriefChart)

        xml = super().to_dom(dom.Poll)
        xml.text = self.text
        xml.mode = self.mode.value
        xml.option = [option.to_dom() for option in self.options]
        return xml


class Option(DSCMS4Model):
    """An option for a poll."""

    class Meta:
        table_name = 'poll_option'

    poll = ForeignKeyField(
        Poll, column_name='poll', backref='options', on_delete='CASCADE')
    text = CharField(255)
    votes = IntegerField(default=0)
    index = IntegerField(default=0)

    @classmethod
    def from_json(cls, json, poll, **kwargs):
        """Creates the image from a JSON-ish dict."""
        record = super().from_json(json, **kwargs)
        record.poll = poll
        return record

    def to_dom(self):
        """Returns an XML DOM of this model."""
        xml = dom.PollOption(self.text)
        xml.id = self.id
        xml.votes = self.votes
        return xml
