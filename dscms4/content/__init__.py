"""Content handlers."""

from dscms4.content import group, terminal

__all__ = ['ROUTES']


ROUTES = group.ROUTES + terminal.ROUTES
