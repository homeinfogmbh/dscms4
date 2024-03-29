"""Handling of groups and group members."""

from dscms4.group import deployment, group, presentation


__all__ = ["ROUTES"]


ROUTES = (*deployment.ROUTES, *group.ROUTES, *presentation.ROUTES)
