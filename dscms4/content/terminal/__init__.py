"""Terminal content management."""

from dscms4.content.terminal import charts, configuration, menu


__all__ = ['ROUTES']


ROUTES = charts.ROUTES + configuration.ROUTES + menu.ROUTES