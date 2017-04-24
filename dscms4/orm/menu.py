"""Menus"""

from peewee import ForeignKeyField, CharField

from .common import DSCMS4Model
from .charts import BaseChart

__all__ = [
    'Menu',
    'ChartItem']


class Menu(DSCMS4Model):
    """Menus tree nodes"""

    class Meta:
        db_table = 'node'

    parent = ForeignKeyField(
        'self', db_column='parent', null=True, default=None)
    name = CharField(255)
    text = CharField(255, null=True, default=None)

    @property
    def root(self):
        """Determines whether this is a root node entry"""
        return self.parent is None

    @property
    def path(self):
        """Yields the path to this menu"""
        if not self.root:
            yield from self.parent.path

        yield self

    @property
    def submenus(self):
        """Yields submenus"""
        return self.__class__.select().where(self.__class__.parent == self)

    @property
    def charts(self):
        """Yields charts"""
        return ChartItem.select().where(ChartItem.menu == self)

    def append(self, name, text=None):
        """Appends the node"""
        node = self.__class__()
        node.parent = self
        node.name = name
        node.text = text
        return node

    def to_dict(self, cascade=False):
        """Converts the model into a JSON compliant dictionary"""
        dictionary = {'name': self.name}

        if self.text is not None:
            dictionary['text'] = self.text

        charts = [chart.to_dict() for chart in self.charts]

        if charts:
            dictionary['charts'] = charts

        if cascade:
            submenus = [m.to_dict(cascade=cascade) for m in self.submenus]

            if submenus:
                dictionary['submenus'] = submenus

        return dictionary


class ChartItem(DSCMS4Model):
    """Menu item mapping"""

    class Meta:
        db_table = 'menu_chart'

    menu = ForeignKeyField(Menu, db_column='menu')
    chart = ForeignKeyField(BaseChart, db_column='chart')

    @property
    def path(self):
        """Yields the path to this menu"""
        yield from self.menu.path
        yield self

    def to_dict(self, cascade=False):
        """Converts the model into a JSON compliant dictionary"""
        return self.chart.id
