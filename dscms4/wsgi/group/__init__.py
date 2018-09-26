"""WSGI handlers for groups and group members."""

from dscms4.wsgi.group import group, member


__all__ = ['ROUTES']


ROUTES = group.ROUTES + member.ROUTES
