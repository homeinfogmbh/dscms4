"""Cleaning chart."""

from enum import Enum

from peewee import TextField, SmallIntegerField, IntegerField
from peeweeplus import EnumField

from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model

__all__ = ['Mode', 'Cleaning']


class Mode(Enum):
    """Possible displaying modes."""

    SHOW = 'show'
    INPUT = 'input'


class Cleaning(DSCMS4Model, Chart):
    """Cleaning chart."""

    class Meta:
        db_table = 'chart_cleaning'

    mode = EnumField(Mode)
    text = TextField(null=True, default=None)
    font_size = SmallIntegerField(default=8)
    text_color = IntegerField(default=0x000000)
