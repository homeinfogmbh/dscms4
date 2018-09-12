#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='dscms4',
    version='latest',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info at homeinfo dot de>',
    maintainer='Richard Neumann',
    maintainer_email='<r dot neumann at homeinfo period de>',
    requires=['his'],
    packages=[
        'dscms4',
        'dscms4.content',
        'dscms4.content.group',
        'dscms4.content.terminal',
        'dscms4.messages',
        'dscms4.orm',
        'dscms4.orm.charts',
        'dscms4.orm.content',
        'dscms4.wsgi',
        'dscms4.wsgi.content',
        'dscms4.wsgi.content.group',
        'dscms4.wsgi.content.terminal',
        'dscms4.wsgi.group',
        'dscms4.wsgi.membership',
        'dscms4.wsgi.menu',
        'dscms4.wsgi.preview'],
    description='HOMEINFO Digital Signage Content Management System v4.')
