"""Configurations controller."""

from his import CUSTOMER, DATA, authenticated, authorized
from his.messages import IncompleteData, InvalidData, MissingData
from peewee import DoesNotExist
from wsgilib import JSON

from dscms4.messages.configuration import NoSuchConfiguration, \
    ConfigurationAdded, ConfigurationPatched, ConfigurationDeleted
from dscms4.orm.configuration import Configuration

__all__ = ['ROUTES']


def _get(ident):
    """Returns the respective configuration."""

    try:
        return Configuration.get(
            (Configuration.customer == CUSTOMER.id)
            & (Configuration.id == ident))
    except DoesNotExist:
        raise NoSuchConfiguration()


@authenticated
@authorized('dscms4')
def lst():
    """Returns a list of IDs of the customer's configurations."""

    return JSON([
        configuration.id for configuration in Configuration.select().where(
            Configuration.customer == CUSTOMER.id)])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective configuration."""

    return JSON(_get(ident).to_dict())


@authenticated
@authorized('dscms4')
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


@authenticated
@authorized('dscms4')
def patch(ident):
    """Modifies an existing configuration."""

    _get(ident).patch(DATA.json)
    return ConfigurationPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Modifies an existing configuration."""

    _get(ident).delete_instance()
    return ConfigurationDeleted()


ROUTES = (
    ('GET', '/configuration', lst, 'list_configurations'),
    ('GET', '/configuration/<int:ident>', get, 'get_configuration'),
    ('POST', '/configuration', add, 'add_configuration'),
    ('PATCH', '/configuration/<int:gid>', patch, 'patch_configuration'),
    ('DELETE', '/configuration/<int:gid>', delete, 'delete_configuration'))
