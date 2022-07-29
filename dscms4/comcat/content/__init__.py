"""Content handling of ComCat accounts."""

from dscms4.comcat.content import charts, configuration, menu


__all__ = ['ROUTES']


ROUTES = sum((configuration.ROUTES, menu.ROUTES), charts.ROUTES)
