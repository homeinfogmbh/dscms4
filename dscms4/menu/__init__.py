"""Handling of menus and related entities."""

from dscms4.menu import base_chart, item, menu


__all__ = ["ROUTES"]


ROUTES = (*base_chart.ROUTES, *item.ROUTES, *menu.ROUTES)
