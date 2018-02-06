"""Cleaning chart."""

from enum import Enum

from peewee import TextField, SmallIntegerField, IntegerField
from peeweeplus import EnumField

from dscms4.orm.charts.common import Chart

__all__ = ['Mode', 'Cleaning']


class Mode(Enum):
    """Possible displaying modes."""

    SHOW = 'show'
    INPUT = 'input'


class Cleaning(Chart):
    """Cleaning chart."""

    class Meta:
        table_name = 'chart_cleaning'

    mode = EnumField(Mode)
    text = TextField(null=True)
    font_size = SmallIntegerField(default=8)
    text_color = IntegerField(default=0x000000)
