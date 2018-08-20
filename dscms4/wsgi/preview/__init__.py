"""Preview access."""

from dscms4.wsgi.preview import terminal, comcat_account


__all__ = ['ROUTES']


ROUTES = terminal.ROUTES + comcat_account.ROUTES
