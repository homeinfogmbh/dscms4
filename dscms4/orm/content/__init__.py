"""Content mappings.

This package provides modules to map
content on so-called "clients".
"""
from dscms4.orm.content import group, terminal

__all__ = ['MODELS']


MODELS = group.MODELS + terminal.MODELS
