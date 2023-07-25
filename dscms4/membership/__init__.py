"""Handling of entities that are associated with certain content."""

from dscms4.membership import base_chart, deployment, group


__all__ = ["ROUTES"]


ROUTES = [*base_chart.ROUTES, *deployment.ROUTES, *group.ROUTES]
