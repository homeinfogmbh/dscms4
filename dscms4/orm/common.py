"""Common ORM models"""

from peewee import PrimaryKeyField, ForeignKeyField
from homeinfo.crm import Customer


__all__ = ['DSCMS4Model', 'CustomerModel']


# Do not derive from peewee.Model to prevent binding of fields
class DSCMS4Model():
    """Basic ORM model for DSCMS4"""

    id = PrimaryKeyField()


# Do not derive from peewee.Model to prevent binding of fields
class CustomerModel(DSCMS4Model):
    """Entity that relates to a customer"""

    customer = ForeignKeyField(Customer, db_column='customer')
