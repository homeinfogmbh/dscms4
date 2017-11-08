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
