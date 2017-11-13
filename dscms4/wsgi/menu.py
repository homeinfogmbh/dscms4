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

    try:
        menu_id = int(ident)
    except TypeError:
        raise NoIdSpecified() from None
    except ValueError:
        raise InvalidId() from None

    try:
        return Menu.get(
            (Menu.customer == customer)
            & (Menu.id == menu_id))
    except DoesNotExist:
        raise NoSuchMenu() from None


def parent_menu_item(dictionary, menu):
    """Returns the respective parent menu item."""

    try:
        parent = int(dictionary['parent'])
    except (KeyError, TypeError):
        parent = None
    else:
        try:
            parent = MenuItem.get(
                (MenuItem.menu == menu) & (MenuItem.parent == parent))
        except DoesNotExist:
            raise NoSuchMenuItem() from None


def menu_item_chart(dictionary, customer):
    """Returns the respective chart for the menu item."""

    try:
        chart = int(dictionary['chart'])
    except (KeyError, TypeError):
        chart = None
    else:
        try:
            chart = BaseChart.get(
                (BaseChart.customer == customer) & (BaseChart.id == chart))
        except DoesNotExist:
            raise NoSuchChart() from None


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
        return get_menu(self.resource, self.customer)

    @property
    @lru_cache(maxsize=1)
    def menu_item(self):
        """Returns the respective menu item."""
        try:
            _, *menu_item_id = self.resource.split('/')
        except (AttributeError, ValueError):
            return None
        else:
            menu_item_id = '/'.join(menu_item_id)

        try:
            menu_item_id = int(menu_item_id)
        except ValueError:
            raise InvalidId() from None

        try:
            return MenuItem.get(
                (MenuItem.menu == self.menu)
                & (MenuItem.id == menu_item_id))
        except DoesNotExist:
            raise NoSuchMenuItem() from None

    def add_menu(self, dictionary):
        """Adds a menu."""
        try:
            menu = Menu.from_dict(dictionary, customer=self.customer)
        except ValueError:
            raise InvalidMenuData() from None
        else:
            menu.save()

        return menu

    def add_menu_item(self, dictionary):
        """Adds a menu item."""
        try:
            menu_item = Menu.from_dict(
                dictionary, menu=self.menu,
                parent=self.parent_menu_item(dictionary, self.menu),
                chart=self.menu_item_chart(dictionary, self.customer))
        except ValueError:
            raise InvalidMenuData() from None
        else:
            menu_item.save()

        return menu_item

    def get(self):
        """Lists menus or returns the selected menu."""
        if self.resource is None:
            return JSON([menu.to_dict() for menu in self.menus])

        return JSON(self.menu.to_dict())

    def post(self):
        """Adds a new menu or menu item."""
        if self.resource is None:
            return self.add_menu(self.data.json)

        return self.add_menu_item(self.data.json)

    def delete(self):
        """Deletes a menu or menu item."""
        if self.resource is None:
            raise NoMenuSpecified() from None
        elif self.menu_item is not None:
            self.menu_item.delete_instance()
            return MenuItemDeleted()

        self.menu.delete_instance()
        return MenuDeleted()
