"""Common ORM models"""

from peewee import PrimaryKeyField, ForeignKeyField

from peeweeplus import MySQLDatabase
from homeinfo.crm import Customer


__all__ = ['DATABASE', 'DSCMS4Model', 'CustomerModel']


DATABASE = MySQLDatabase('dscms4')


class DSCMS4Model():
    """Basic ORM model for DSCMS4.

     Not derived from peewee.Model to prevent binding of fields.
     """

    id = PrimaryKeyField()

    class Meta:
        database = DATABASE
        schema = database.database


# Do not derive from peewee.Model to prevent binding of fields
class CustomerModel(DSCMS4Model):
    """Entity that relates to a customer.

     Not derived from peewee.Model to prevent binding of fields.
     """

    customer = ForeignKeyField(Customer, db_column='customer')
