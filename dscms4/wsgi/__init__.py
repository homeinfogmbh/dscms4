"""WSGI application routes."""

from wsgilib import Application

from dscms4.wsgi import configuration, content, charts, group, media, menu, \
    terminal

__all__ = ['APPLICATION']


APPLICATION = Application('DSCMS4')
ROUTES =

for route, method, function in chain(
        configuration.ROUTES, content.ROUTES, charts.ROUTES):
        # Configuration endpoint.
        # Content endpoint.
        # Charts endpoint.
        # Group endpoint.,
        # Media endpoint.
        # TODO: implement.
        # Menu endpoint.
        ('/menu', 'GET', menu.list),
        ('/menu/<int:ident>', 'GET', menu.get),
        ('/menu', 'POST', menu.add),
        ('/menu/<int:gid>', 'PATCH', menu.patch),
        ('/menu/<int:gid>', 'DELETE', menu.delete),
        # Terminal endpoint.
        ('/terminals', 'GET', terminal.list),
        ('/terminals/<int:tid>', 'GET', terminal.get)):
    APPLICATION.route(route, methods=[method])(function)
