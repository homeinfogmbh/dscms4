#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='dsmcs4',
    version='latest',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info at homeinfo dot de>',
    maintainer='Richard Neumann',
    maintainer_email='<r dot neumann at homeinfo period de>',
    requires=['his'],
    packages=[
        'dscms4',
        'dscms4.messages',
        'dscms4.orm',
        'dscms4.orm.charts',
        'dscms4.orm.content',
        'dscms4.wsgi',
        'dscms4.wsgi.content',
        'dscms4.wsgi.content.group',
        'dscms4.wsgi.content.terminal',
        'dscms4.wsgi.group',
        'dscms4.wsgi.menu'],
    data_files=[
        ('/usr/lib/systemd/system', ['files/dscms4.service']),
        ('/etc/his.d/locale', ['files/locales/dscms4.ini']),
        ('/etc/his.d/locale/dscms4.d', [
            'files/locales/charts.ini',
            'files/locales/configuration.ini',
            'files/locales/content.ini',
            'files/locales/group.ini',
            'files/locales/media.ini',
            'files/locales/menu.ini',
            'files/locales/terminal.ini'])],
    description='HOMEINFO Digital Signage Content Management System v4.')
