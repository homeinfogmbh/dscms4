"""Company structure"""

from peewee import ForeignKeyField, CharField
from homeinfo.crm import Customer
from .common import DSCMS4Model


class OrganizationUnit(DSCMS4Model):
    """An organizational unit"""

    customer = ForeignKeyField(Customer, db_column='customer')
    parent = ForeignKeyField(
        'self', db_column='parent',
         null=True, default=None)
    ident = CharField(255)
    name = CharField(255)
    annotation = CharField(255, null=True, default=None)
