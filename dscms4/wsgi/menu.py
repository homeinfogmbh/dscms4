"""DSCMS4 WSGI handlers for menus."""

from functools import lru_cache

from peewee import DoesNotExist
from wsgilib import JSON

from dscms4.orm.charts import BaseChart
from dscms4.orm.exceptions import NoSuchChart
from dscms4.orm.menu import Menu, MenuItem
from dscms4.wsgi.common import DSCMS4Service
from dscms4.wsgi.messages import NoIdSpecified, InvalidId, NoSuchMenu

__all__ = ['MenuHandler']


def get_menu(customer, ident):
    """Returns the respective menu by its ID."""

    if customer is None or ident is None:
        return None

    try:
        return Menu.get((Menu.customer == customer) & (Menu.id == ident))
    except DoesNotExist:
        raise NoSuchMenu() from None


def parent_menu_item(dictionary, menu):
    """Returns the respective parent menu item."""

    if dictionary is None or menu is None:
        return None

    try:
        parent = int(dictionary['parent'])
    except (KeyError, TypeError):
        return None

    try:
        return MenuItem.get(
            (MenuItem.menu == menu) & (MenuItem.parent == parent))
    except DoesNotExist:
        raise NoSuchMenuItem() from None


def menu_item_chart(dictionary, customer):
    """Returns the respective chart for the menu item."""

    if dictionary is None or customer is None:
        return None

    try:
        chart = int(dictionary['chart'])
    except (KeyError, TypeError):
        return None

    try:
        return BaseChart.get(
            (BaseChart.customer == customer) & (BaseChart.id == chart))
    except DoesNotExist:
        raise NoSuchChart() from None


@ROUTER.route('/menu/[id:int]')
class MenuHandler(DSCMS4Service):
    """Handles the menus."""

    @property
    def menus(self):
        """Yields menus of the current customer."""
        return Menu.select().where(Menu.customer == self.customer)

    @property
    @lru_cache(maxsize=1)
    def menu(self):
        """Returns the selected menu."""
        return get_menu(self.customer, self.vars['id'])

    def get(self):
        """Lists menus or returns the selected menu."""
        if self.resource is None:
            return JSON([menu.to_dict() for menu in self.menus])

        return JSON(self.menu.to_dict())

    def post(self):
        """Adds a new menu or menu item."""
        try:
            menu = Menu.from_dict(self.data.json, customer=self.customer)
        except ValueError:
            raise InvalidMenuData() from None
        else:
            menu.save()
            return MenuAdded()

    def delete(self):
        """Deletes a menu or menu item."""
        if self.menu is None:
            raise NoMenuSpecified() from None

        self.menu.delete_instance()
        return MenuDeleted()


@ROUTER.route('/menu/<menu_id:int>/[id:int]')
class MenuItemHandler(DSCMS4Service):
    """Handles the menus."""

    @property
    @lru_cache(maxsize=1)
    def menu(self):
        """Returns the respective menu."""
        return get_menu(self.customer, self.vars['menu_id'])

    @property
    def menu_items(self):
        """Yields menus of the current customer."""
        return MenuItem.select().where(MenuItem.menu == self.menu)

    @property
    @lru_cache(maxsize=1)
    def menu_item(self):
        """Returns the respective menu item."""
        try:
            return MenuItem.get(
                (MenuItem.menu == self.menu)
                & (MenuItem.id == self.vars['menu_id']))
        except DoesNotExist:
            raise NoSuchMenuItem() from None

    def get(self):
        """Lists menus or returns the selected menu."""
        if self.resource is None:
            return JSON([menu.to_dict() for menu in self.menus])

        return JSON(self.menu.to_dict())

    def post(self):
        """Adds a new menu or menu item."""
        try:
            menu_item = Menu.from_dict(
                self.data.json, menu=self.menu,
                parent=parent_menu_item(dictionary, self.menu),
                chart=menu_item_chart(dictionary, self.customer))
        except ValueError:
            raise InvalidMenuData() from None
        else:
            menu_item.save()
            return MenuItemAdded()

    def delete(self):
        """Deletes a menu or menu item."""
        if self.menu_item is None:
            return NoMenuItemSpecified()

        self.menu_item.delete_instance()
        return MenuItemDeleted()
