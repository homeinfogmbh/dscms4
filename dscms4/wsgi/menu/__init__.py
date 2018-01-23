"""DSCMS4 WSGI handlers for menus."""

from dscms4.wsgi.menu import menu, item

__all__ = ['ROUTES']


ROUTES = menu.ROUTES + item.ROUTES
