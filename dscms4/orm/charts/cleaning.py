"""Cleaning chart."""

from enum import Enum

from peewee import Model, TextField, SmallIntegerField, IntegerField
from peeweeplus import EnumField

from dscms4.orm.charts.common import Chart

__all__ = ['Mode', 'Cleaning']


DEFAULT_FONT_SIZE = 8
DEFAULT_COLOR = 0x000000


class Mode(Enum):
    """Possible displaying modes."""

    SHOW = 'show'
    INPUT = 'input'


class Cleaning(Model, Chart):
    """Cleaning chart."""

    class Meta:
        db_table = 'chart_cleaning'

    mode = EnumField(Mode)
    text = TextField(null=True, default=None)
    font_size = SmallIntegerField(default=DEFAULT_FONT_SIZE)
    text_color = IntegerField(default=DEFAULT_COLOR)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new record from the provided dictionary."""
        chart = super().from_dict(dictionary)
        chart.mode = dictionary['mode']
        chart.text = dictionary.get('text')
        chart.font_size = dictionary.get('font_size', DEFAULT_FONT_SIZE)
        chart.text_color = dictionary.get('text_color', DEFAULT_COLOR)
        return chart

    @property
    def dictionary(self):
        """Returns a dictionary representation of this record."""
        return {
            'mode': self.mode.value,
            'text': self.text,
            'font_size': self.font_size,
            'text_color': self.text_color}
