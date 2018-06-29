"""DSCMS4 configuration."""

from configlib import INIParser

__all__ = ['LOG_FORMAT', 'CONFIG']


LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
CONFIG = INIParser('/etc/dscms4.conf')
