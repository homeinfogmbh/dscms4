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
    'RelatedKeyField',
    'DSCMS4Model',
    'CustomerModel',
    'RelatedModel']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


def create_tables(models, fail_silently=True):
    """Creates the tables for the provided models."""

    for model in models:
        model.create_table(fail_silently=fail_silently)


class RelatedKeyField(ForeignKeyField):
    """A specialized foreign key field to identify
    paths to a related customer model.
    """

    pass


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
    def cselect(cls, *fields):
        """Returns a selection with additional filtering
        for the current HIS customer context.
        """
        return cls.select(*fields).where(cls.customer == CUSTOMER.id)

    @classmethod
    def cget(cls, *query, **filters):
        """Returns a single record with additional filtering
        for the current HIS customer context.
        """
        return cls.get(*query + ((cls.customer == CUSTOMER.id),), **filters)

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
            raise ValueError('No customer specified.')

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


class RelatedModel(DSCMS4Model):
    """Base class for models that are related to customer models."""

    @classmethod
    def get_related_model(cls):
        """Returns the related key."""
        for field in cls._meta.fields.values():
            if isinstance(field, RelatedKeyField):
                return field.rel_model

        return None

    @classmethod
    def _relation_path(cls):
        """Yields the respective models leading to the customer model."""
        rel_model = cls.get_related_model()

        while rel_model is not None:
            yield rel_model
            rel_model = rel_model.get_related_model()

        yield rel_model

    @classmethod
    def cselect(cls, *fields):
        """Returns a selection with additional filtering
        for the current HIS customer context.
        """
        select_query = cls.select(*fields)

        for rel_model in cls._relation_path():
            select_query = select_query.join(rel_model)

        # Select customer on last related model.
        return select_query.where(rel_model.customer == CUSTOMER.id)

    @classmethod
    def cget(cls, *query, **filters):
        """Returns a single record with additional filtering
        for the current HIS customer context.
        """
        select_query = cls.cselect()

        if query:
            select_query = select_query.where(*query)

        if filters:
            select_query = select_query.filter(**filters)

        return select_query.get()
