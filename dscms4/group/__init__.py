"""Handling of groups and group members."""

from dscms4.group import group, system, tree


__all__ = ['ROUTES']


ROUTES = group.ROUTES + system.ROUTES + tree.ROUTES
