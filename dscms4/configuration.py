"""Configurations controller."""

from flask import request

from cmslib.functions.configuration import get_configuration
from cmslib.functions.configuration import list_configurations
from cmslib.messages.configuration import CONFIGURATION_ADDED
from cmslib.messages.configuration import CONFIGURATION_PATCHED
from cmslib.messages.configuration import CONFIGURATION_DELETED
from cmslib.orm.configuration import Configuration
from his import JSON_DATA, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES', 'list_configurations', 'get_configuration']


@authenticated
@authorized('dscms4')
def list_():
    """Returns a list of IDs of the customer's configurations."""

    configurations = list_configurations()

    if 'assoc' in request.args:
        return JSON({
            configuration.id: configuration.to_json(fk_fields=False)
            for configuration in configurations})

    return JSON([
        configuration.to_json(fk_fields=False)
        for configuration in configurations])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective configuration."""

    return JSON(get_configuration(ident).to_json(cascade=True))


@authenticated
@authorized('dscms4')
def add():
    """Adds a new configuration."""

    transaction = Configuration.from_json(JSON_DATA)
    transaction.commit()
    return CONFIGURATION_ADDED.update(id=transaction.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Modifies an existing configuration."""

    configuration = get_configuration(ident)
    transaction = configuration.patch_json(JSON_DATA)
    transaction.commit()
    return CONFIGURATION_PATCHED


@authenticated
@authorized('dscms4')
def delete(ident):
    """Modifies an existing configuration."""

    get_configuration(ident).delete_instance()
    return CONFIGURATION_DELETED


ROUTES = (
    ('GET', '/configuration', list_),
    ('GET', '/configuration/<int:ident>', get),
    ('POST', '/configuration', add),
    ('PATCH', '/configuration/<int:ident>', patch),
    ('DELETE', '/configuration/<int:ident>', delete)
)
