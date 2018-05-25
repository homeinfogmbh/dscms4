"""Configurations controller."""

from his import CUSTOMER, DATA, authenticated, authorized
from his.messages import IncompleteData, InvalidData, MissingData

from wsgilib import JSON

from dscms4.messages.configuration import NoSuchConfiguration, \
    ConfigurationAdded, ConfigurationPatched, ConfigurationDeleted
from dscms4.orm.configuration import Configuration

__all__ = ['get_configuration', 'ROUTES']


def get_configuration(ident):
    """Returns the respective configuration."""

    try:
        return Configuration.get(
            (Configuration.customer == CUSTOMER.id)
            & (Configuration.id == ident))
    except Configuration.DoesNotExist:
        raise NoSuchConfiguration()


@authenticated
@authorized('dscms4')
def list_():
    """Returns a list of IDs of the customer's configurations."""

    return JSON([
        configuration.to_dict() for configuration
        in Configuration.select().where(
            Configuration.customer == CUSTOMER.id)])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective configuration."""

    return JSON(get_configuration(ident).to_dict())


@authenticated
@authorized('dscms4')
def add():
    """Adds a new configuration."""

    ident = None

    try:
        for record in Configuration.from_dict(CUSTOMER.id, DATA.json):
            record.save()

            if ident is None and isinstance(record, Configuration):
                ident = record.id
    except MissingData as missing_data:
        raise IncompleteData(missing_data.missing)
    except InvalidData as invalid_data:
        raise InvalidData(invalid_data.invalid)

    return ConfigurationAdded(id=ident)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Modifies an existing configuration."""

    try:
        for record in get_configuration(ident).patch(DATA.json):
            record.save()
    except MissingData as missing_data:
        raise IncompleteData(missing_data.missing)
    except InvalidData as invalid_data:
        raise InvalidData(invalid_data.invalid)

    return ConfigurationPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Modifies an existing configuration."""

    get_configuration(ident).delete_instance()
    return ConfigurationDeleted()


ROUTES = (
    ('GET', '/configuration', list_, 'list_configurations'),
    ('GET', '/configuration/<int:ident>', get, 'get_configuration'),
    ('POST', '/configuration', add, 'add_configuration'),
    ('PATCH', '/configuration/<int:ident>', patch, 'patch_configuration'),
    ('DELETE', '/configuration/<int:ident>', delete, 'delete_configuration'))
