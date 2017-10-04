"""Menus."""

from peewee import Model, ForeignKeyField, CharField

from .common import DSCMS4Model, CustomerModel
from .charts import Chart
from .exceptions import MissingData

__all__ = [
    'Menu',
    'MenuItem',
    'MenuItemChart']


class Menu(JSONModel, CustomerModel):
    """Menus trees."""

    name = CharField(255)
    description = CharField(255, null=True, default=None)


class MenuItem(JSONModel, DSCMS4Model):
    """A menu item."""

    class Meta:
        db_table = 'menu_item'

    menu = ForeignKeyField(Menu, db_column='menu')
    parent = ForeignKeyField(
        'self', db_column='parent', null=True, default=None)
    name = CharField(255)
    icon = EnumField(ICONS, nulll=True, default=None)
    text_color = IntegerField(default=0x000000)
    background_color = IntegerField(default=0xffffff)

    @property
    def root(self):
        """Determines whether this is a root node entry."""
        return self.parent is None

    @property
    def path(self):
        """Yields the path to this menu."""
        if not self.root:
            for parent in self.parent.path:
                yield parent

        yield self

    @property
    def submenus(self):
        """Yields submenus."""
        return self.__class__.select().where(self.__class__.parent == self)

    @property
    def charts(self):
        """Yields charts."""
        return MenuItemChart.charts_for(self)

    def append(self, name, icon=None, text_color=None, background_color=None):
        """Appends the node."""
        menu_item = self.__class__()
        menu_item.parent = self
        menu_item.name = name
        menu_item.icon = icon

        if text_color is not None:
            menu_item.text_color = text_color

        if background_color is not None:
            menu_item.background_color = background_color

        return menu_item


class MenuItemChart(JSONModel, DSCMS4Model):
    """Menu item <> Chart mapping."""

    class Meta:
        db_table = 'menu_item_chart'

    menu = ForeignKeyField(Menu, db_column='menu')
    chart = ForeignKeyField(Chart, db_column='chart')

    @classmethod
    def charts_for(cls, menu):
        """Yields charts for the specified menu."""
        for menu_item_chart in cls.select().where(cls.menu == menu):
            yield menu_item_chart.chart

    @property
    def path(self):
        """Yields the path to this menu."""
        yield from self.menu.path
        yield self
