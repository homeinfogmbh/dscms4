"""Menus, menu items and chart members."""

from enum import Enum

from peewee import Model, ForeignKeyField, CharField, IntegerField

from peeweeplus import ForeignKeyConstraint, EnumField

from .common import DSCMS4Model, CustomerModel
from .charts import BaseChart
from .exceptions import CircularPedigreeError

__all__ = [
    'Icons',
    'Menu',
    'MenuItem',
    'MODELS']


class Icons(Enum):
    """Valid icons."""

    COOL_ICON = 'cool icon'


class Menu(Model, CustomerModel):
    """Menus trees."""

    name = CharField(255)
    description = CharField(255, null=True, default=None)

    @property
    def items(self):
        """Yields this menu's items."""
        return MenuItem.by_menu(self)

    def to_dict(self):
        """Returns the menu as a dictionary."""
        dictionary = super().to_dict()
        dictionary['items'] = [item.to_dict() for item in self.items]
        return dictionary


class MenuItem(Model, DSCMS4Model):
    """A menu item."""

    class Meta:
        db_table = 'menu_item'

    menu = ForeignKeyField(Menu, db_column='menu')
    parent = ForeignKeyField(
        'self', db_column='parent', null=True, default=None)
    name = CharField(255)
    icon = EnumField(Icons, default=None)
    text_color = IntegerField(default=0x000000)
    background_color = IntegerField(default=0xffffff)
    chart = ForeignKeyField(
        BaseChart, null=True, default=None, db_column='chart',
        on_delete=ForeignKeyConstraint.SET_NULL)

    @classmethod
    def from_dict(cls, dictionary, menu=None, parent=None, chart=None):
        """Creates a new menu item from the provided dictionary."""
        menu_item = super().from_dict(dictionary)
        menu_item.menu = menu
        menu_item.parent = parent
        menu_item.chart = chart
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

    def move(self, parent):
        """Moves this menu entry to a new parent."""
        if parent in self.tree:
            raise CircularPedigreeError()

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

    def to_dict(self):
        """Returns a dictionary representation for the respective menu."""
        dictionary = super().to_dict(
            ignore=(self.__class__.menu, self.__class__.parent))
        dictionary['chart'] = self.chart.tto_dict() if self.chart else None
        dictionary['items'] = [item.to_dict() for item in self.submenus]
        return dictionary


MODELS = (Menu, MenuItem)
