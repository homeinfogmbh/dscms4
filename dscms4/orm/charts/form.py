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

    typ = EnumField(Type, db_column='type')
