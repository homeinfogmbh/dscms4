"""WSGI application routes."""

from itertools import chain

from wsgilib import Application

from dscms4.wsgi import charts, configuration, content, file, group, menu, \
    terminal

__all__ = ['APPLICATION', 'ROUTES']


APPLICATION = Application('DSCMS4', cors=True, debug=True)
ROUTES = (
    charts.ROUTES + configuration.ROUTES + content.ROUTES + file.ROUTES
    + group.ROUTES + menu.ROUTES + terminal.ROUTES)
APPLICATION.add_routes(ROUTES)
