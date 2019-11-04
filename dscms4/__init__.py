"""Digital Signage Content Management System, version 4.

A web application to allow customers to edit
and organize digital signage content.
"""
from itertools import chain
from logging import INFO, basicConfig

from his import Application

from dscms4 import base_chart_schedule
from dscms4 import chart_types
from dscms4 import charts
from dscms4 import configuration
from dscms4 import content
from dscms4 import deployment
from dscms4 import group
from dscms4 import membership
from dscms4 import menu
from dscms4 import preview
from dscms4 import schedule
from dscms4 import settings


__all__ = ['APPLICATION', 'ROUTES']


LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
APPLICATION = Application('DSCMS4', debug=True)
ROUTES = (
    base_chart_schedule.ROUTES + chart_types.ROUTES + charts.ROUTES
    + configuration.ROUTES + content.ROUTES + deployment.ROUTES + group.ROUTES
    + membership.ROUTES + menu.ROUTES + preview.ROUTES + schedule.ROUTES
    + settings.ROUTES)
APPLICATION.add_routes(ROUTES)


@APPLICATION.before_first_request
def _init_logger():
    """Initializes the logger."""

    basicConfig(level=INFO, format=LOG_FORMAT)
