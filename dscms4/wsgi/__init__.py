"""WSGI application routes."""

from itertools import chain

from his import Application

from dscms4.wsgi import charts
from dscms4.wsgi import configuration
from dscms4.wsgi import content
from dscms4.wsgi import group
from dscms4.wsgi import management
from dscms4.wsgi import membership
from dscms4.wsgi import menu
from dscms4.wsgi import preview
from dscms4.wsgi import previewgen
from dscms4.wsgi import terminal


__all__ = ['APPLICATION', 'ROUTES']


APPLICATION = Application('DSCMS4', cors=True, debug=True)
ROUTES = (
    charts.ROUTES + configuration.ROUTES + content.ROUTES + group.ROUTES
    + management.ROUTES + membership.ROUTES + menu.ROUTES + preview.ROUTES
    + previewgen.ROUTES + terminal.ROUTES)
APPLICATION.add_routes(ROUTES)
