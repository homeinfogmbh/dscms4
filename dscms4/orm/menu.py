"""Menus, menu items and chart members."""

from logging import getLogger

from peewee import ForeignKeyField, CharField, IntegerField

from dscms4 import dom
from dscms4.orm.common import DSCMS4Model, CustomerModel
from dscms4.orm.charts import BaseChart
from dscms4.orm.exceptions import CircularReferenceError, OrphanedBaseChart, \
    AmbiguousBaseChart
from dscms4.orm.util import chart_of

__all__ = ['UNCHANGED', 'Menu', 'MenuItem', 'MODELS']


UNCHANGED = object()
LOGGER = getLogger('Menu')


class Menu(CustomerModel):
    """Menus trees."""

    name = CharField(255)
    description = CharField(255, null=True)

    @property
    def items(self):
        """Yields this menu's root items."""
        return MenuItem.select().where(
            (MenuItem.menu == self) & (MenuItem.parent >> None))

    def to_json(self):
        """Returns the menu as a dictionary."""
        dictionary = super().to_json()
        dictionary['items'] = [item.to_json() for item in self.items]
        return dictionary

    def to_dom(self):
        """Returns an XML DOM of the model."""
        xml = dom.Menu()
        xml.name = self.name
        xml.description = self.description
        xml.item = [item.to_dom() for item in self.items]
        return xml


class MenuItem(DSCMS4Model):
    """A menu item."""

    class Meta:
        table_name = 'menu_item'

    menu = ForeignKeyField(Menu, column_name='menu', on_delete='CASCADE')
    parent = ForeignKeyField(
        'self', column_name='parent', null=True, backref='children')
    name = CharField(255)
    icon = CharField(255, null=True)
    text_color = IntegerField(default=0x000000)
    background_color = IntegerField(default=0xffffff)
    index = IntegerField(default=0)
    JSON_KEYS = {'textColor': text_color, 'backgroundColor': background_color}

    @classmethod
    def from_json(cls, json, menu, parent=None, **kwargs):
        """Creates a new menu item from the provided dictionary."""
        menu_item = super().from_json(json, **kwargs)
        menu_item.menu = menu
        menu_item.parent = parent
        return menu_item

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
    def tree(self):
        """Recursively yields all submenus."""
        yield self

        for child in self.children:
            yield from child.tree

    @property
    def charts(self):
        """Yields the respective charts."""
        for menu_item_chart in self.menu_item_charts:
            base_chart = menu_item_chart.base_chart

            try:
                yield chart_of(base_chart)
            except OrphanedBaseChart:
                LOGGER.error('Base chart #%i is orphaned.', base_chart.id)
            except AmbiguousBaseChart:
                LOGGER.error('Base chart #%i is ambiguous.', base_chart.id)

    def move(self, parent):
        """Moves this menu entry to a new parent."""
        if parent in self.tree:
            raise CircularReferenceError()

        self.parent = parent
        self.menu = self.parent.menu
        self.save()

    def append(self, child):
        """Appends a new submenu."""
        return child.move(self)

    def remove(self, update_children=False):
        """Removes this menu item."""
        if update_children:
            for child in self.children:
                child.move(self.parent)

        return self.delete_instance()

    def patch_json(self, dictionary, *args, menu=UNCHANGED, parent=UNCHANGED,
                   **kwargs):
        """Patches the menu item."""
        super().patch_json(dictionary, *args, **kwargs)

        if menu is not UNCHANGED:
            self.menu = menu

        if parent is not UNCHANGED:
            self.parent = parent

        return self

    def to_json(self, *args, **kwargs):
        """Returns a dictionary representation for the respective menu."""
        dictionary = super().to_json(*args, **kwargs)
        dictionary['charts'] = [
            chart.to_json() for chart in self.menu_item_charts]
        dictionary['items'] = [
            item.to_json(*args, **kwargs) for item in self.children]
        return dictionary

    def to_dom(self):
        """Returns an XML DOM of the model."""
        xml = dom.MenuItem()
        xml.name = self.name
        xml.icon = self.icon
        xml.text_color = self.text_color
        xml.background_color = self.background_color
        xml.index = self.index
        xml.item = [item.to_dom() for item in self.children]
        xml.chart = [chart.to_dom() for chart in self.menu_item_charts]
        return xml


class MenuItemChart(DSCMS4Model):
    """Mapping in-between menu items and base charts."""

    class Meta:
        table_name = 'menu_item_chart'

    menu_item = ForeignKeyField(
        MenuItem, null=True, column_name='menu_item',
        backref='menu_item_charts', on_delete='CASCADE')
    base_chart = ForeignKeyField(
        BaseChart, null=True, column_name='base_chart', on_delete='CASCADE')
    index = IntegerField(default=0)
    JSON_KEYS = {'menuItem': menu_item, 'baseChart': base_chart}

    def to_json(self):
        """Returns a JSON-ish dictionary."""
        chart = chart_of(self.base_chart)
        dictionary = chart.to_json(brief=True)
        dictionary['index'] = self.index
        return dictionary

    def to_dom(self):
        """Returns an XML DOM of the model."""
        xml = dom.MenuItemChart()
        chart = chart_of(self.base_chart)
        xml.id = chart.id
        xml.type = type(chart).__name__
        xml.index = self.index
        return xml


MODELS = (Menu, MenuItem, MenuItemChart)
