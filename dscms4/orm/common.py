"""Common ORM models."""

from peewee import PrimaryKeyField, ForeignKeyField

from homeinfo.crm import Customer
from peeweeplus import MySQLDatabase, JSONModel

from dscms4.config import CONFIG


__all__ = [
    'DATABASE',
    'create_tables',
    'save',
    'DSCMS4Model',
    'CustomerModel',
    'RecordGroup']


DATABASE = MySQLDatabase(
    CONFIG['db']['db'], host=CONFIG['db']['host'], user=CONFIG['db']['user'],
    passwd=CONFIG['db']['passwd'], closing=True)


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

    id = PrimaryKeyField()

    @classmethod
    def by_id(cls, ident):
        """Yields records for the respective ID."""
        return cls.get(cls.id == ident)


class CustomerModel(DSCMS4Model):
    """Entity that relates to a customer."""

    customer = ForeignKeyField(Customer, column_name='customer')

    @classmethod
    def from_dict(cls, customer, dictionary, **kwargs):
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

    def _save(self):
        """Saves the records and yields their IDs."""
        for record in self:
            yield record.save()

    def save(self):
        """Saves the records."""
        return tuple(self._save())
