"""Configurations controller."""

from flask import request

from cmslib.functions.configuration import get_configuration
from cmslib.functions.configuration import get_configurations
from cmslib.orm.configuration import Configuration
from his import authenticated, authorized, require_json
from wsgilib import JSON, JSONMessage, get_bool


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Returns a list of IDs of the customer's configurations."""

    if get_bool('assoc'):
        return JSON({
            configuration.id: configuration.to_json(fk_fields=False)
            for configuration in get_configurations()
        })

    return JSON([
        configuration.to_json(fk_fields=False)
        for configuration in get_configurations()])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the respective configuration."""

    return JSON(get_configuration(ident).to_json(cascade=True))


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds a new configuration."""

    transaction = Configuration.from_json(request.json)
    transaction.commit()
    return JSONMessage('Configuration added.', id=transaction.id, status=201)


@authenticated
@authorized('dscms4')
@require_json(dict)
def patch(ident: int) -> JSONMessage:
    """Modifies an existing configuration."""

    configuration = get_configuration(ident)
    transaction = configuration.patch_json(request.json)
    transaction.commit()
    return JSONMessage('Configuration patched.', status=200)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Modifies an existing configuration."""

    get_configuration(ident).delete_instance()
    return JSONMessage('Configuration deleted.', status=200)


ROUTES = [
    ('GET', '/configuration', list_),
    ('GET', '/configuration/<int:ident>', get),
    ('POST', '/configuration', add),
    ('PATCH', '/configuration/<int:ident>', patch),
    ('DELETE', '/configuration/<int:ident>', delete)
]
