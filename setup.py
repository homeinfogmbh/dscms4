#! /usr/bin/env python3

from distutils.core import setup
from homeinfo.lib.misc import GitInfo

version, author, author_email, *_ = GitInfo()

setup(
    name='his.dsmcs4',
    version=version,
    author=author,
    author_email=author_email,
    requires=['his'],
    package_dir={'his.mods': ''},
    packages=['his.mods.dscms4'],
    data_files=[('/etc/his.d/locale', ['files/etc/his.d/locale/fs.ini'])],
    description='HOMEINFO Digital Signage Content Management System v4')
