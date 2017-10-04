"""Menus, menu items and chart members."""

from enum import Enum

from peewee import ForeignKeyField, CharField, IntegerField

from peeweeplus import JSONModel, EnumField

from .common import DSCMS4Model, CustomerModel
from .charts import Chart

__all__ = [
    'Menu',
    'MenuItem',
    'MenuItemChart']


class Icons(Enum):
    """Valid icons."""

    COOL_ICON = 'cool icon'


class Menu(JSONModel, CustomerModel):
    """Menus trees."""

    name = CharField(255)
    description = CharField(255, null=True, default=None)

    def to_dict(self, cascade=False):
        """Returns the menu as a dictionary."""
        dictionary = super().to_dict()

        if cascade:
            dictionary['items'] = [
                menu_item.to_dict(cascade=cascade)
                for menu_item in MenuItem.by_menu(self)]

        return dictionary


class MenuItem(JSONModel, DSCMS4Model):
    """A menu item."""

    class Meta:
        db_table = 'menu_item'

    menu = ForeignKeyField(Menu, db_column='menu')
    parent = ForeignKeyField(
        'self', db_column='parent', null=True, default=None)
    name = CharField(255)
    icon = EnumField(Icons, nulll=True, default=None)
    text_color = IntegerField(default=0x000000)
    background_color = IntegerField(default=0xffffff)

    @classmethod
    def by_menu(cls, menu):
        """Yields menu items belonging to the respective menu."""
        return cls.select().where(cls.menu == menu)

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

    def to_dict(self, cascade=False):
        """Returns a dictionary representation for the respective menu."""
        dictionary = super().to_dict()
        dictionary['charts'] = [chart.id for chart in self.charts]

        if cascade:
            dictionary['items'] = [
                item.to_dict(cascade=cascade) for item in self.submenus]

        return dictionary


class MenuItemChart(JSONModel, DSCMS4Model):
    """Menu item <> Chart mapping."""

    class Meta:
        db_table = 'menu_item_chart'

    menu_item = ForeignKeyField(MenuItem, db_column='menu')
    chart = ForeignKeyField(Chart, db_column='chart')

    @classmethod
    def charts_for(cls, menu_item):
        """Yields charts for the specified menu."""
        for menu_item_chart in cls.select().where(cls.menu_item == menu_item):
            yield menu_item_chart.chart
