"""Common ORM models."""

from peewee import ForeignKeyField

from mdb import Customer
from peeweeplus import MySQLDatabase, JSONModel

from dscms4.config import CONFIG


__all__ = [
    'DATABASE',
    'create_tables',
    'save',
    'DSCMS4Model',
    'CustomerModel',
    'RecordGroup']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


def create_tables(models, fail_silently=True):
    """Creates the tables for the provided models."""

    for model in models:
        model.create_table(fail_silently=fail_silently)


def save(models):
    """Saves an iterable of models."""
    for model in models:
        model.save()


class DSCMS4Model(JSONModel):
    """Base Model for the DSCMS4 database."""

    class Meta:
        database = DATABASE
        schema = database.database

    def __str__(self):
        """Returns the models's ID and class."""
        return '{}@{}'.format(self.id, self.__class__.__name__)

    @classmethod
    def by_id(cls, ident):
        """Yields records for the respective ID."""
        return cls.get(cls.id == ident)


class CustomerModel(DSCMS4Model):
    """Entity that relates to a customer."""

    customer = ForeignKeyField(Customer, column_name='customer')

    @classmethod
    def from_json(cls, dictionary, customer, **kwargs):
        """Creates a new record from the provided dictionary and customer."""
        record = super().from_dict(dictionary, **kwargs)
        record.customer = customer
        return record

    @classmethod
    def by_customer(cls, customer):
        """Yields records for the respective customer."""
        return cls.select().where(cls.customer == customer)


class RecordGroup(tuple):
    """A group of records that shall be handled together."""

    def save(self, *args, **kwargs):
        """Saves the records."""
        for record in self:
            record.save(*args, **kwargs)
