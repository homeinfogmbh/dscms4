"""DSCMS4 WSGI handlers for menus."""

from dscms4.wsgi.menu import menu, item, charts
from dscms4.wsgi.menu.menu import get_menu

__all__ = ['get_menu', 'ROUTES']


ROUTES = menu.ROUTES + item.ROUTES + charts.ROUTES
