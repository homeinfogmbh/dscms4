"""DSCMS4 WSGI handlers for menus."""

from dscms4.menu import menu, item, charts

__all__ = ['ROUTES']


ROUTES = menu.ROUTES + item.ROUTES + charts.ROUTES
