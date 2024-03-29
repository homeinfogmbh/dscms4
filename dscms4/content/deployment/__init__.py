"""Deployments content management."""

from dscms4.content.deployment import base_chart, configuration, menu


__all__ = ["ROUTES"]


ROUTES = (*base_chart.ROUTES, *configuration.ROUTES, *menu.ROUTES)
