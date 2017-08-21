"""Configurations"""

from peewee import Model

from .common import CustomerModel

__all__ = ['Configuration']


class Configuration(Model, CustomerModel):
    """Customer configuration for charts"""

    # TODO: Add configurations for all possible charts
    pass
