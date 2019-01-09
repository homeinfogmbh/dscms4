"""Handling of groups and group members."""

from dscms4.group import group, member, tree


__all__ = ['ROUTES']


ROUTES = group.ROUTES + member.ROUTES + tree.ROUTES
