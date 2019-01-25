"""Digital Signage Content Management System, version 4.

A web application to allow customers to edit
and organize digital signage content.
"""

from itertools import chain

from his import Application

from dscms4 import charts
from dscms4 import comcat_account
from dscms4 import configuration
from dscms4 import content
from dscms4 import group
from dscms4 import membership
from dscms4 import menu
from dscms4 import preview
from dscms4 import previewgen
from dscms4 import settings
from dscms4 import terminal


__all__ = ['APPLICATION', 'ROUTES']


APPLICATION = Application('DSCMS4', debug=True)
ROUTES = (
    charts.ROUTES + comcat_account.ROUTES + configuration.ROUTES
    + content.ROUTES + group.ROUTES + membership.ROUTES + menu.ROUTES
    + preview.ROUTES + previewgen.ROUTES + settings.ROUTES + terminal.ROUTES)
APPLICATION.add_routes(ROUTES)
