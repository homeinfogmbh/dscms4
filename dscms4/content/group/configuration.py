"""Management of configurations in groups."""

from flask import request

from cmslib import GroupConfiguration
from cmslib import get_configuration
from cmslib import get_group
from cmslib import get_group_configuration
from cmslib import get_group_configurations
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage, get_int, require_json


__all__ = ["ROUTES"]


@authenticated
@authorized("dscms4")
def get(ident: int) -> JSON:
    """Returns the request group configuration."""

    return JSON(get_group_configuration(ident, CUSTOMER.id).to_json(cascade=True))


@authenticated
@authorized("dscms4")
def list_() -> JSON:
    """Returns a list of IDs of the configurations in the respective group."""

    return JSON(
        [
            record.to_json()
            for record in get_group_configurations(CUSTOMER.id, group=get_int("group"))
        ]
    )


@authenticated
@authorized("dscms4")
@require_json(dict)
def add() -> JSONMessage:
    """Adds the configuration to the respective group."""

    group = get_group(request.json.pop("group"), CUSTOMER.id)
    configuration = get_configuration(request.json.pop("configuration"), CUSTOMER.id)
    record = GroupConfiguration(group=group, configuration=configuration)
    record.save()
    return JSONMessage("Group configuration added.", id=record.id, status=201)


@authenticated
@authorized("dscms4")
def delete(ident: int) -> JSONMessage:
    """Deletes the configuration from the respective group."""

    get_group_configuration(ident, CUSTOMER.id).delete_instance()
    return JSONMessage("Group configuration deleted.", status=200)


ROUTES = [
    ("GET", "/content/group/configuration", list_),
    ("GET", "/content/group/configuration/<int:ident>", get),
    ("POST", "/content/group/configuration", add),
    ("DELETE", "/content/group/configuration/<int:ident>", delete),
]
