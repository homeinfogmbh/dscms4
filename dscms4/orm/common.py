"""Common ORM models"""

from peewee import PrimaryKeyField, ForeignKeyField

from peeweeplus import MySQLDatabase
from homeinfo.crm import Customer


__all__ = ['DATABASE', 'create_tables', 'DSCMS4Model', 'CustomerModel']


DATABASE = MySQLDatabase('dscms4')


def create_tables(models, fail_silently=True):
    """Creates the tables for the provided models."""

    for model in models:
        model.create_table(fail_silently=fail_silently)


class DSCMS4Model:
    """Basic ORM model for DSCMS4.

     Not derived from peewee.Model to prevent binding of fields.
     """

    class Meta:
        database = DATABASE
        schema = database.database

    id = PrimaryKeyField()

    @classmethod
    def by_id(cls, ident):
        """Yields records for the respective ID."""
        return cls.get(cls.id == ident)

    def to_dict(self):
        """Returns a JSON compliant dictionary."""
        return {'id': self.id}


# Do not derive from peewee.Model to prevent binding of fields
class CustomerModel(DSCMS4Model):
    """Entity that relates to a customer.

     Not derived from peewee.Model to prevent binding of fields.
     """

    customer = ForeignKeyField(Customer, db_column='customer')

    @classmethod
    def by_customer(cls, customer):
        """Yields records for the respective customer."""
        return cls.select().where(cls.customer == customer)

    def to_dict(self, cascade=False):
        """Returns a JSON compliant dictionary."""
        dictionary = super().to_dict()

        if cascade:
            dictionary['customer'] = self.customer.to_dict()
        else:
            dictionary['customer'] = self.customer.id

        return dictionary
