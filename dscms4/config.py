"""DSCMS4 configuration."""

from configlib import INIParser

__all__ = ['CONFIG']


CONFIG = INIParser('/etc/dscms4.conf')
