"""WSGI handlers for groups and group members."""

from dscms4.wsgi.group import group, member
from dscms4.wsgi.group.group import get_group

__all__ = ['get_group', 'ROUTES']


ROUTES = group.ROUTES + member.ROUTES
