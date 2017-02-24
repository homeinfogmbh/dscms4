"""Configurations"""

from peewee import ForeignKeyField

from homeinfo.crm import Customer

from .common import DSCMS4Model

__all__ = ['Configuration']


class Configuration(DSCMS4Model):
    """Customer configuration for charts"""

    customer = ForeignKeyField(Customer, db_column='customer')
    # TODO: Add configurations for all possible charts
