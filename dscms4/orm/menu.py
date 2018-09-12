"""Menus, menu items and chart members."""

from logging import getLogger

from peewee import ForeignKeyField, CharField, IntegerField

from peeweeplus import MissingKeyError

from dscms4 import dom
from dscms4.exceptions import OrphanedBaseChart, AmbiguousBaseChart
from dscms4.messages.common import CircularReference
from dscms4.messages.menu import NoMenuSpecified, DifferentMenusError
from dscms4.orm.common import CustomerModel, DSCMS4Model
from dscms4.orm.charts import BaseChart
from dscms4.orm.util import chart_of


__all__ = ['Menu', 'MenuItem', 'MODELS']


LOGGER = getLogger('Menu')
UNCHANGED = object()


class Menu(CustomerModel):
    """Menus trees."""

    name = CharField(255)
    description = CharField(255, null=True)

    @property
    def root_items(self):
        """Yields this menu's root items."""
        return self.items.where(MenuItem.parent >> None)

    def to_json(self, *args, items=False, **kwargs):
        """Returns the menu as a dictionary."""
        json = super().to_json(*args, **kwargs)

        if items:
            json['items'] = [
                item.to_json(charts=True, children=True, fk_fields=False)
                for item in self.root_items]

        return json

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

    menu = ForeignKeyField(
        Menu, column_name='menu', on_delete='CASCADE', backref='items')
    parent = ForeignKeyField(
        'self', column_name='parent', null=True, on_delete='CASCADE',
        backref='children')
    name = CharField(255)
    icon = CharField(255, null=True)
    text_color = IntegerField(default=0x000000)
    background_color = IntegerField(default=0xffffff)
    index = IntegerField(default=0)

    @classmethod
    def from_json(cls, json, **kwargs):
        """Creates a new menu item from the provided dictionary."""
        menu = json.pop('menu', None)
        parent = json.pop('parent', None)
        menu_item = super().from_json(json, **kwargs)
        menu_item.move(menu=menu, parent=parent)
        return menu_item

    @property
    def root(self):
        """Determines whether this is a root node entry."""
        return self.menu is not None

    @property
    def childrens_children(self):
        """Recursively yields all submenus."""
        for child in self.children:
            for childrens_child in child.childrens_children:
                yield childrens_child

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

    def _get_menu(self, menu):
        """Returns the respective menu."""
        if menu is None:
            raise NoMenuSpecified()

        if menu is UNCHANGED:
            return self.menu

        return Menu.get(
            (Menu.customer == self.menu.customer) & (Menu.id == menu))

    def _get_parent(self, parent):
        """Returns the respective parent."""
        if parent is None:
            return None

        if parent is UNCHANGED:
            return self.parent

        cls = type(self)
        return cls.select().join(Menu).where(
            (Menu.customer == self.menu.customer) & (cls.id == parent)).get()

    def move(self, *, menu=UNCHANGED, parent=UNCHANGED):
        """Moves the menu item to another menu and / or parent."""
        menu = self._get_menu(menu)
        parent = self._get_parent(parent)

        if parent is not None:
            if parent.menu != menu:
                raise DifferentMenusError()

            if parent in self.childrens_children:
                raise CircularReference()

        self.menu = menu
        self.parent = parent

        for child in self.childrens_children:
            child.menu = menu
            child.save()

        self.save()

    def delete_instance(self, update_children=False, **kwargs):
        """Removes this menu item."""
        if update_children:
            for child in self.children:
                child.move(parent=self.parent)

        return super().delete_instance(**kwargs)

    def patch_json(self, json, **kwargs):
        """Patches the menu item."""
        menu = json.pop('menu', UNCHANGED)
        parent = json.pop('parent', UNCHANGED)
        super().patch_json(json, **kwargs)
        self.move(menu=menu, parent=parent)

    def to_json(self, charts=False, children=False, **kwargs):
        """Returns a JSON-ish dictionary."""
        json = super().to_json(**kwargs)

        if charts:
            json['charts'] = [
                chart.to_json() for chart in self.charts
                if not chart.base.trashed]    # Exclude trashed charts.

        if children:
            json['items'] = [
                item.to_json(charts=charts, children=children, **kwargs)
                for item in self.children]

        return json

    def to_dom(self):
        """Returns an XML DOM of the model."""
        xml = dom.MenuItem()
        xml.name = self.name
        xml.icon = self.icon
        xml.text_color = self.text_color
        xml.background_color = self.background_color
        xml.index = self.index
        xml.item = [item.to_dom() for item in self.children]
        xml.chart = [
            menu_item_chart.to_dom() for menu_item_chart
            in self.menu_item_charts]
        return xml


class MenuItemChart(DSCMS4Model):
    """Mapping in-between menu items and base charts."""

    class Meta:
        table_name = 'menu_item_chart'

    menu_item = ForeignKeyField(
        MenuItem, column_name='menu_item', backref='menu_item_charts',
        on_delete='CASCADE')
    base_chart = ForeignKeyField(
        BaseChart, column_name='base_chart', on_delete='CASCADE')
    index = IntegerField(default=0)

    @classmethod
    def from_json(cls, json, **kwargs):
        """Creates a record from a JSON-ish dictionary."""
        try:
            menu_item = MenuItem.get(MenuItem.id == json.pop('menuItem'))
        except KeyError:
            raise MissingKeyError('menuItem')

        try:
            base_chart = BaseChart.get(BaseChart.id == json.pop('baseChart'))
        except KeyError:
            raise MissingKeyError('baseChart')

        menu_item_chart = super().from_json(json, **kwargs)
        menu_item_chart.menu_item = menu_item
        menu_item_chart.base_chart = base_chart
        return menu_item_chart

    def to_json(self):
        """Returns a JSON-ish dictionary."""
        chart = chart_of(self.base_chart)
        json = chart.to_json(brief=True)
        json['index'] = self.index
        return json

    def to_dom(self):
        """Returns an XML DOM of the model."""
        xml = dom.MenuItemChart()
        chart = chart_of(self.base_chart)
        xml.id = chart.id
        xml.type = type(chart).__name__
        xml.index = self.index
        return xml


MODELS = (Menu, MenuItem, MenuItemChart)
