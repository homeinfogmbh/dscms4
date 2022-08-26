"""Digital Signage Content Management System, version 4.

A web application to allow customers to edit
and organize digital signage content.
"""
from logging import INFO, basicConfig

from cmslib import ERRORS
from comcatlib import init_fcm
from his import Application

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
from dscms4 import vfs


__all__ = ['APPLICATION', 'ROUTES']


LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
APPLICATION = Application('DSCMS4')
ROUTES = (
    *chart_types.ROUTES, *charts.ROUTES, *configuration.ROUTES,
    *content.ROUTES, *deployment.ROUTES, *group.ROUTES, *membership.ROUTES,
    *menu.ROUTES, *preview.ROUTES, *schedule.ROUTES, *settings.ROUTES,
    *vfs.ROUTES
)
APPLICATION.add_routes(ROUTES)


@APPLICATION.before_first_request
def _init_logger():
    """Initializes the logger."""

    basicConfig(level=INFO, format=LOG_FORMAT)
    init_fcm()


for exception, function in ERRORS.items():
    APPLICATION.register_error_handler(exception, function)
