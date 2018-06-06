"""Charts for forms."""

from enum import Enum

from peeweeplus import EnumField

from dscms4 import dom
from dscms4.orm.charts.common import Chart

__all__ = ['Mode', 'Form']


class Mode(Enum):
    """Form type."""

    REPAIR = 'repair'
    TENANT_TO_TENANT = 'tenant2tenant'


class Form(Chart):
    """A form chart."""

    class Meta:
        table_name = 'chart_form'

    mode = EnumField(Mode, column_name='mode')

    def to_dom(self):
        """Returns an XML DOM of this chart."""
        xml = super().to_dom(dom.Form)
        xml.mode = self.mode
        return xml
