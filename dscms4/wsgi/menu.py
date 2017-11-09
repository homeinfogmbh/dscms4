"""DSCMS4 WSGI handlers for menus."""

from peewee import DoesNotExist
from wsgilib import JSON

from dscms4.wsgi.common import DSCMS4Service
from dscms4.wsgi.messages import NoIdSpecified, InvalidId, NoSuchMenu


class Menu(DSCMS4Service):
    """Handles the menus."""

    @property
    def menus(self):
        """Yields menus of the current customer."""
        return Menu.select().where(Menu.customer == self.customer)

    @property
    def menu(self):
        """Returns the selected menu."""
        try:
            menu_id = int(self.resource)
        except TypeError:
            raise NoIdSpecified() from None
        except ValueError:
            raise InvalidId() from None
        else:
            try:
                return Menu.get(
                    (Menu.customer == self.customer) &
                    (Menu.id == menu_id))
            except DoesNotExist:
                raise NoSuchMenu() from None

    def get(self):
        """Lists menus or returns the selected menu."""
        if self.resource is None:
            return JSON([menu.to_dict() for menu in self.menus])

        return JSON(self.menu.to_dict())
