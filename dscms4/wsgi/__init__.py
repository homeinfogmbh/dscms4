"""WSGI application routes."""

from itertools import chain

from wsgilib import Application

from dscms4.wsgi import charts, configuration, content, group, menu, terminal

__all__ = ['APPLICATION', 'ROUTES']


APPLICATION = Application('DSCMS4')
ROUTES = (
    charts.ROUTES + configuration.ROUTES + content.ROUTES + group.ROUTES
    + menu.ROUTES + terminal.ROUTES)
APPLICATION.add_routes(ROUTES)
