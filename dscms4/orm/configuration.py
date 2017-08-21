"""Configurations"""

from peewee import Model

from .common import DSCMS4Model

__all__ = ['Configuration']


class Configuration(Model, DSCMS4Model):
    """Customer configuration for charts"""

    # TODO: Add configurations for all possible charts
    pass
