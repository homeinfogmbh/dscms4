"""WSGI application routes."""

from itertools import chain

from wsgilib import Application

from dscms4.wsgi import charts, configuration, content, group, media, menu, \
    terminal

__all__ = ['APPLICATION']


APPLICATION = Application('DSCMS4')
APPLICATION.add_routes(chain(
    charts.ROUTES, configuration.ROUTES, content.ROUTES, group.ROUTES,
    media.ROUTES, menu.ROUTES, terminal.ROUTES))
