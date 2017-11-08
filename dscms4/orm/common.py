"""Common ORM models"""

from peewee import PrimaryKeyField, ForeignKeyField

from peeweeplus import MySQLDatabase, JSONSerializable
from homeinfo.crm import Customer


__all__ = [
    'DATABASE',
    'create_tables',
    'save',
    'DSCMS4Model',
    'CustomerModel']


DATABASE = MySQLDatabase('dscms4')


def create_tables(models, fail_silently=True):
    """Creates the tables for the provided models."""

    for model in models:
        model.create_table(fail_silently=fail_silently)


def save(models):
    """Saves an iterable of models."""
    for model in models:
        model.save()


class DSCMS4Model(JSONSerializable):
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


class CustomerModel(DSCMS4Model):
    """Entity that relates to a customer.

     Not derived from peewee.Model to prevent binding of fields.
     """

    customer = ForeignKeyField(Customer, db_column='customer')

    @classmethod
    def by_customer(cls, customer):
        """Yields records for the respective customer."""
        return cls.select().where(cls.customer == customer)

    def to_dict(self):
        """Returns a JSON compliant dictionary."""
        dictionary = super().to_dict()
        dictionary['customer'] = self.customer.id
        return dictionary
