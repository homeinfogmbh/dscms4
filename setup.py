#! /usr/bin/env python3
"""Install script."""

from setuptools import setup


setup(
    name='dscms4',
    use_scm_version={
        "local_scheme": "node-and-timestamp"
    },
    setup_requires=['setuptools_scm'],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info at homeinfo dot de>',
    maintainer='Richard Neumann',
    maintainer_email='<r dot neumann at homeinfo period de>',
    install_requires=[
        'cmslib',
        'flask',
        'functoolsplus',
        'his',
        'hwdb',
        'mdb',
        'peewee',
        'previewlib',
        'wsgilib'
    ],
    packages=[
        'dscms4',
        'dscms4.content',
        'dscms4.content.group',
        'dscms4.content.deployment',
        'dscms4.group',
        'dscms4.membership',
        'dscms4.menu',
        'dscms4.preview'
    ],
    description='HOMEINFO Digital Signage Content Management System v4.'
)
