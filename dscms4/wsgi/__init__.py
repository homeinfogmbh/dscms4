"""WSGI application routes."""

from wsgilib import Application

from dscms4.wsgi import content, charts, group, media, menu, terminal

__all__ = ['APPLICATION']


APPLICATION = Application('DSCMS4')
ROUTING_TABLE = (
    # Charts endpoint.
    ('/charts', 'GET', charts.list),
    ('/charts/<int:ident>', 'GET', charts.get),
    ('/charts', 'POST', charts.add),
    ('/charts/<int:ident>', 'DELETE', charts.delete),
    ('/charts/<int:ident>', 'PATCH', charts.patch),
    # Content endpoint.
    ('/content/group/<int:gid>/chart', 'GET', content.group.chart.list),
    ('/content/group/<int:gid>/chart', 'POST', content.group.chart.add),
    ('/content/group/<int:gid>/chart/<int:ident>', 'DELETE',
     content.group.chart.delete),
    ('/content/group/<int:gid>/configuration', 'GET',
     content.group.configuration.list),
    ('/content/group/<int:gid>/configuration', 'POST',
     content.group.configuration.add),
    ('/content/group/<int:gid>/configuration/<int:ident>', 'DELETE',
     content.group.configuration.delete),
    # TODO: continue to implement.
    # Terminal endpoint.
    ('/terminals', 'GET', terminal.list),
    ('/terminals/<int:tid>', 'GET', terminal.get))


# Apply all routes to the application.
for route, method, function in ROUTING_TABLE:
    APPLICATION.route(route, methods=[method])(function)
