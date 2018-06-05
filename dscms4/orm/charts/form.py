"""Charts for forms."""

from enum import Enum

from peeweeplus import EnumField

from dscms4.orm.charts.common import Chart

__all__ = ['Type', 'Form']


class Type(Enum):
    """Form type."""

    REPAIR = 'repair'
    TENANT_TO_TENANT = 'tenant2tenant'


class Form(Chart):
    """A form chart."""

    class Meta:
        table_name = 'chart_form'

    type_ = EnumField(Type, column_name='type')
