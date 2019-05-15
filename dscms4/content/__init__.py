"""Handling of content associated with certain entities."""

from dscms4.content import deployment, group


__all__ = ['ROUTES']


ROUTES = deployment.ROUTES + group.ROUTES
