"""Handling of groups and group members."""

from dscms4.group import group, terminal, tree


__all__ = ['ROUTES']


ROUTES = group.ROUTES + terminal.ROUTES + tree.ROUTES
