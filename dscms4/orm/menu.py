"""Menus, menu items and chart members."""

from logging import getLogger

from peewee import ForeignKeyField, CharField, IntegerField

from .common import DSCMS4Model, CustomerModel
from .charts import BaseChart
from .exceptions import CircularReferenceError, OrphanedBaseChart, \
    AmbiguousBaseChart
from .util import chart_of

__all__ = ['UNCHANGED', 'Menu', 'MenuItem', 'MODELS']


UNCHANGED = object()
LOGGER = getLogger('Menu')


class Menu(CustomerModel):
    """Menus trees."""

    name = CharField(255)
    description = CharField(255, null=True)

    @property
    def items(self):
        """Yields this menu's items."""
        return MenuItem.by_menu(self)

    def to_dict(self, brief=False):
        """Returns the menu as a dictionary."""
        if brief:
            return {'id': self.id}

        dictionary = super().to_dict()
        dictionary['items'] = [item.to_dict() for item in self.items]
        return dictionary


class MenuItem(DSCMS4Model):
    """A menu item."""

    class Meta:
        table_name = 'menu_item'

    menu = ForeignKeyField(Menu, column_name='menu', on_delete='CASCADE')
    parent = ForeignKeyField('self', column_name='parent', null=True)
    name = CharField(255)
    icon = CharField(255, null=True)
    text_color = IntegerField(default=0x000000)
    background_color = IntegerField(default=0xffffff)
    index = IntegerField(default=0)

    @classmethod
    def from_dict(cls, menu, dictionary, parent=None):
        """Creates a new menu item from the provided dictionary."""
        menu_item = super().from_dict(dictionary)
        menu_item.menu = menu
        menu_item.parent = parent
        return menu_item

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
    def children(self):
        """Yields child menu items."""
        return self.__class__.select().where(self.__class__.parent == self)

    @property
    def tree(self):
        """Recursively yields all submenus."""
        yield self

        for child in self.children:
            yield from child.tree

    @property
    def base_charts(self):
        """Yields the respective charts."""
        for menu_item_chart in MenuItemChart.select().where(
                MenuItemChart.menu_item == self):
            yield menu_item_chart.base_chart

    @property
    def charts(self):
        """Yields the respective charts."""
        for base_chart in self.base_charts:
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

    def patch(self, dictionary, *args, menu=UNCHANGED, parent=UNCHANGED,
              **kwargs):
        """Patches the menu item."""
        super().patch(dictionary, *args, **kwargs)

        if menu is not UNCHANGED:
            self.menu = menu

        if parent is not UNCHANGED:
            self.parent = parent

        return self

    def to_dict(self, *args, **kwargs):
        """Returns a dictionary representation for the respective menu."""
        dictionary = super().to_dict(*args, **kwargs)
        dictionary['charts'] = [chart.to_dict() for chart in self.charts]
        dictionary['items'] = [item.id for item in self.children]
        dictionary['root'] = self.root
        return dictionary


class MenuItemChart(DSCMS4Model):
    """Mapping in-between menu items and base charts."""

    class Meta:
        table_name = 'menu_item_chart'

    menu_item = ForeignKeyField(
        MenuItem, null=True, column_name='menu_item', on_delete='CASCADE')
    base_chart = ForeignKeyField(
        BaseChart, null=True, column_name='base_chart', on_delete='CASCADE')
    index = IntegerField(default=0)

    @classmethod
    def add(cls, menu_item, base_chart):
        """Creates a new menu item chart."""
        menu_item_chart = cls()
        menu_item_chart.menu_item = menu_item
        menu_item_chart.base_chart = base_chart
        return menu_item_chart


MODELS = (Menu, MenuItem, MenuItemChart)
