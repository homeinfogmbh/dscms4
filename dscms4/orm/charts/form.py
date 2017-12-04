"""Charts for forms."""

from enum import Enum

from peeweeplus import EnumField

from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model

__all__ = ['Type', 'Form']


class Type(Enum):
    """Form type."""

    REPAIR = 'repair'
    TENANT_TO_TENANT = 'tenant2tenant'


class Form(DSCMS4Model, Chart):
    """A form chart."""

    class Meta:
        db_table = 'chart_form'

    typ = EnumField(Type, db_column='type')
