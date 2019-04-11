"""Handling of content associated with certain entities."""

from dscms4.content import group, system


__all__ = ['ROUTES']


ROUTES = group.ROUTES + system.ROUTES
