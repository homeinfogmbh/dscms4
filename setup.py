#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='dsmcs4',
    version='latest',
    author='Richard Neumann',
    requires=['his'],
    packages=[
        'dscms4',
        'dscms4.orm'],
    description='HOMEINFO Digital Signage Content Management System v4')
