"""Common ORM models."""

from peewee import Model, PrimaryKeyField, ForeignKeyField

from peeweeplus import MySQLDatabase, JSONSerializable
from homeinfo.crm import Customer

from dscms4.config import CONFIG


__all__ = [
    'DATABASE',
    'create_tables',
    'save',
    'DSCMS4Model',
    'CustomerModel']


DATABASE = MySQLDatabase(
    CONFIG['db']['db'],
    host=CONFIG['db']['host'],
    user=CONFIG['db']['user'],
    passwd=CONFIG['db']['passwd'])


def create_tables(models, fail_silently=True):
    """Creates the tables for the provided models."""

    for model in models:
        model.create_table(fail_silently=fail_silently)


def save(models):
    """Saves an iterable of models."""
    for model in models:
        model.save()


class DSCMS4Model(Model):
    """Base Model for the DSCMS4 database."""

    class Meta:
        database = DATABASE
        schema = database.database

    id = PrimaryKeyField()

    @classmethod
    def by_id(cls, ident):
        """Yields records for the respective ID."""
        return cls.get(cls.id == ident)


class CustomerModel:
    """Entity that relates to a customer.

     Not derived from peewee.Model to prevent binding of fields.
     """

    customer = ForeignKeyField(Customer, db_column='customer')

    @classmethod
    def from_dict(cls, dictionary, customer=None):
        """Creates a new record from the provided dictionary and customer."""
        record = super().from_dict(dictionary)
        record.customer = customer
        return record

    @classmethod
    def by_customer(cls, customer):
        """Yields records for the respective customer."""
        return cls.select().where(cls.customer == customer)
