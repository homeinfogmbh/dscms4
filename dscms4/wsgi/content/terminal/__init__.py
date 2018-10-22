"""Group content management."""

from dscms4.wsgi.content.terminal import charts, configuration, menu


__all__ = ['ROUTES']


ROUTES = charts.ROUTES + configuration.ROUTES + menu.ROUTES
