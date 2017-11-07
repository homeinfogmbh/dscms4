"""Charts for forms."""

from enum import Enum

from peewee import Model
from peeweeplus import EnumField

from dscms4.orm.charts.common import Chart


class Type(Enum):
    """Form type."""

    REPAIR = 'repair'
    TENANT_TO_TENANT = 'tenant2tenant'


class Form(Model, Chart):
    """A form chart."""

    class Meta:
        db_table = 'chart_form'

    typ = EnumField(Type, db_column='type')

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new record from the provided dictionary."""
        chart = super().from_dict(dictionary)
        chart.typ = dictionary['type']
        return chart

    @property
    def dictionary(self):
        """Returns a JSON-ish dictionary."""
        return {'type': self.typ.value}
