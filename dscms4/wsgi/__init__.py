"""WSGI application routes."""

from itertools import chain

from his import Application

from dscms4.wsgi import charts, configuration, content, group, membership, \
    menu, preview, previewgen, terminal


__all__ = ['APPLICATION', 'ROUTES']


APPLICATION = Application('DSCMS4', cors=True, debug=True)
ROUTES = (
    charts.ROUTES + configuration.ROUTES + content.ROUTES + group.ROUTES
    + membership.ROUTES + menu.ROUTES + preview.ROUTES + previewgen.ROUTES
    + terminal.ROUTES)
APPLICATION.add_routes(ROUTES)
