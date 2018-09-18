"""Common ORM models."""

from flask import has_request_context
from peewee import ForeignKeyField

from his import CUSTOMER
from mdb import Customer
from peeweeplus import MySQLDatabase, JSONModel

from dscms4.config import CONFIG, LOGGER
from dscms4.messages.common import InvalidReference


__all__ = [
    'UNCHANGED',
    'DATABASE',
    'create_tables',
    'DSCMS4Model',
    'CustomerModel']


UNCHANGED = object()
DATABASE = MySQLDatabase.from_config(CONFIG['db'])


def create_tables(models, fail_silently=True):
    """Creates the tables for the provided models."""

    for model in models:
        model.create_table(fail_silently=fail_silently)


class DSCMS4Model(JSONModel):
    """Base Model for the DSCMS4 database."""

    class Meta:
        """Sets database and schema."""
        database = DATABASE
        schema = database.database

    def __str__(self):
        """Returns the models's ID and class."""
        return '{}@{}'.format(self.id, type(self).__name__)


class CustomerModel(DSCMS4Model):
    """Entity that relates to a customer."""

    customer = ForeignKeyField(Customer, column_name='customer')

    @classmethod
    def from_json(cls, json, *, customer=None, **kwargs):
        """Creates a new record from the provided
        JSON-ish dictionary for a customer.

        If a customer is not specified and a flask request
        context exists, the current HIS customer will be used.
        """
        if customer is not None:
            LOGGER.warning('Explicitely set customer to: %s.', customer)
        elif has_request_context():
            customer = CUSTOMER.id
        else:
            raise TypeError('No customer specified.')

        record = super().from_json(json, **kwargs)
        record.customer = customer
        return record

    def get_peer(self, record_or_id):
        """Ensures that the provided record or ID is of the same
        model and for the same customer as this record itself.
        """
        if record_or_id is None:
            return None

        cls = type(self)

        if isinstance(record_or_id, cls):
            if record_or_id.customer == self.customer:
                return record_or_id

            raise InvalidReference()

        try:
            return cls.get(
                (cls.id == record_or_id) & (cls.customer == self.customer))
        except cls.DoesNotExist:
            raise InvalidReference()
