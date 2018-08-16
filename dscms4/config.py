"""DSCMS4 configuration."""

from logging import INFO, basicConfig, getLogger

from configlib import INIParser

__all__ = ['CONFIG', 'LOG_FORMAT', 'LOGGER']


CONFIG = INIParser('/etc/dscms4.conf')
LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
basicConfig(level=INFO, format=LOG_FORMAT)
LOGGER = getLogger('dscms4')
