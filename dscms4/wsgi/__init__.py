"""WSGI application routes."""

from wsgilib import Application

from dscms4.wsgi.charts import get_charts, get_chart, add_chart, delete_chart,\
    patch_chart
from dscms4.wsgi.content.group.charts import get_group_charts, \
    add_group_chart, delete_group_chart
from dscms4.wsgi.content.group.configuration import get_group_configurations, \
    add_group_configuration, delete_group_configuration

__all__ = ['APPLICATION']


APPLICATION = Application('DSCMS4')

# Charts endpoint.
APPLICATION.route('/charts', methods=['GET'])(get_charts)
APPLICATION.route('/charts/<int:ident>', methods=['GET'])(get_chart)
APPLICATION.route('/charts', methods=['POST'])(add_chart)
APPLICATION.route('/charts/<int:ident>', methods=['DELETE'])(delete_chart)
APPLICATION.route('/charts/<int:ident>', methods=['PATCH'])(patch_chart)

# Content endpoint.
APPLICATION.route('/content/group/<int:gid>/chart', methods=['GET'])(
    get_group_charts)
APPLICATION.route('/content/group/<int:gid>/chart', methods=['POST'])(
    add_group_chart)
APPLICATION.route(
    '/content/group/<int:gid>/chart/<int:ident>', methods=['DELETE'])(
    delete_group_chart)
APPLICATION.route('/content/group/<int:gid>/configuration', methods=['GET'])(
    get_group_configurations)
APPLICATION.route('/content/group/<int:gid>/configuration', methods=['POST'])(
    add_group_configuration)
APPLICATION.route(
    '/content/group/<int:gid>/configuration/<int:ident>', methods=['DELETE'])(
    delete_group_configuration)
