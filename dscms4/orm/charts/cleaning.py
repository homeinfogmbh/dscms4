"""Cleaning chart."""

from enum import Enum

from peewee import CharField, TextField, SmallIntegerField, IntegerField
from peeweeplus import EnumField

from dscms4.dom import Cleaning as CleaningDOM
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

    title = CharField(255)
    mode = EnumField(Mode)
    text = TextField(null=True)
    font_size = SmallIntegerField(default=8)
    text_color = IntegerField(default=0x000000)

    def to_dom(self):
        """Returns an XML DOM of this chart."""
        dom = super().to_dom(CleaningDOM)
        dom.mode = self.mode.value
        dom.text = self.text
        dom.font_size = self.font_size
        dom.text_color = self.text_color
        return dom
