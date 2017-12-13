"""Configurations controller."""

from his import CUSTOMER
from wsgilib import JSON

from dscms4.wsgi.messages.configuration import NoSuchConfiguration, \
    ConfigurationAdded, ConfigurationPatched, ConfigurationDeleted
from dscms4.orm.configuration import Configuration
from dscms4.orm.exceptions import InvalidData, MissingData

__all__ = ['ROUTES']


def _get(ident):
    """Returns the respective configuration."""

    try:
        return Configuration.get(
            (Configuration.customer == CUSTOMER.id)
            & (Configuration.id == ident))
    except DoesNotExist:
        raise NoSuchConfiguration()


def lst():
    """Returns a list of IDs of the customer's configurations."""

    return JSON([
        configuration.id for configuration in Configuration.select().where(
            Configuration.customer == CUSTOMER.id)])


def get(ident):
    """Returns the respective configuration."""

    return JSON(_get(ident).to_dict())


def add():
    """Adds a new configuration."""

    try:
        for record in Configuration.from_dict(DATA.json, CUSTOMER.id):
            record.save()
    except MissingData as missing_data:
        raise IncompleteData(missing_data.missing)
    except InvalidData as invalid_data:
        raise InvalidData(invalid_data.invalid)

    return ConfigurationAdded()


def patch(ident):
    """Modifies an existing configuration."""

    _get(ident).patch(DATA.json)
    return ConfigurationPatched()


def delete(ident):
    """Modifies an existing configuration."""

    _get(ident).delete_instance()
    return ConfigurationDeleted()


ROUTES = (
    ('/configuration', 'GET', lst),
    ('/configuration/<int:ident>', 'GET', get),
    ('/configuration', 'POST', add),
    ('/configuration/<int:gid>', 'PATCH', patch),
    ('/configuration/<int:gid>', 'DELETE', delete))
