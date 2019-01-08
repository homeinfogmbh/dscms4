"""Preview access."""

from dscms4.preview import comcat_account, group, terminal


__all__ = ['ROUTES']


ROUTES = comcat_account.ROUTES + group.ROUTES + terminal.ROUTES
