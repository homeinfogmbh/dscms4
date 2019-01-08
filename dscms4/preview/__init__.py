"""Preview access."""

from dscms4.wsgi.preview import comcat_account, group, terminal


__all__ = ['ROUTES']


ROUTES = comcat_account.ROUTES + group.ROUTES + terminal.ROUTES
