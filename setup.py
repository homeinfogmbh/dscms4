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
        'dscms4.wsgi'],
    description='HOMEINFO Digital Signage Content Management System v4.')
