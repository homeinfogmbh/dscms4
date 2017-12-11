"""WSGI application routes."""

from wsgilib import Application

from dscms4.wsgi.charts import get_charts, get_chart, add_chart, delete_chart,\
    patch_chart

__all__ = ['APPLICATION']


APPLICATION = Application('DSCMS4')
APPLICATION.route('/charts', methods=['GET'])(get_charts)
APPLICATION.route('/charts/<int:ident>', methods=['GET'])(get_chart)
APPLICATION.route('/charts', methods=['POST'])(add_chart)
APPLICATION.route('/charts/<int:ident>', methods=['DELETE'])(delete_chart)
APPLICATION.route('/charts/<int:ident>', methods=['PATCH'])(patch_chart)
