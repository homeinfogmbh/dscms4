"""Group content management."""

from dscms4.wsgi.content.terminal import charts, configuration, menu, ticker

__all__ = ['ROUTES']


ROUTES = charts.ROUTES + configuration.ROUTES + menu.ROUTES + ticker.ROUTES
