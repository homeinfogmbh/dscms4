"""Handling of content associated with certain entities."""

from dscms4.content import comcat_account, group, terminal


__all__ = ['ROUTES']


ROUTES = comcat_account.ROUTES + group.ROUTES + terminal.ROUTES
