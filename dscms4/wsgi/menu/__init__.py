"""Menu controllers."""

from dscms4.wsgi.menu import menu, item

__all__ = ['ROUTES']


ROUTES = menu.ROUTES + item.ROUTES
