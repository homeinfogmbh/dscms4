"""Common ORM models."""

from flask import has_request_context
from peewee import ForeignKeyField

from his import CUSTOMER
from mdb import Customer
from peeweeplus import MySQLDatabase, JSONModel

from dscms4.config import CONFIG, LOGGER
from dscms4.messages.common import InvalidReference


__all__ = [
    'DATABASE',
    'create_tables',
    'DSCMS4Model',
    'CustomerModel']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


def _log_warning():
    """Logs warning and info message if no request context is
    available and filtering for customer context is omitted.
    """

    LOGGER.warning('Querying outside of request context.')
    LOGGER.info('Will not filter for customers.')


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

    @classmethod
    def by_id(cls, ident):
        """Yields records for the respective ID."""
        return cls.get(cls.id == ident)


class CustomerModel(DSCMS4Model):
    """Entity that relates to a customer."""

    customer = ForeignKeyField(Customer, column_name='customer')

    @classmethod
    def from_json(cls, json, customer, **kwargs):
        """Creates a new record from the provided
        JSON-ish dictionary and customer.
        """
        record = super().from_dict(json, **kwargs)
        record.customer = customer
        return record

    @classmethod
    def get(cls, *query, **filters):
        """Returns the respective records for the customer in the current
        HIS context iff no customer was explicitely specified in the filters.
        """
        if has_request_context():
            return super().get(*query, customer=CUSTOMER.id, **filters)

        _log_warning()
        return super().get(*query, **filters)


    @classmethod
    def select(cls, *fields):
        """Returns a selection with additional filtering for
        the current HIS customer iff within HIS context.
        """
        model_select = super().select(*fields)

        if has_request_context():
            where = cls.customer == CUSTOMER.id
            model_select._where = where     # pylint: disable=W0212
        else:
            _log_warning()

        return model_select

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
