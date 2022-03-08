"""Group Controllers."""

from flask import request

from cmslib import Group, get_group, get_groups
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage, get_bool, require_json


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists IDs of groups of the respective customer."""

    if get_bool('tree'):
        return JSON([
            group.json_tree for group in get_groups(CUSTOMER.id).where(
                Group.parent >> None
            )
        ])

    return JSON([group.to_json() for group in get_groups(CUSTOMER.id)])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the respective group."""

    return JSON(get_group(ident, CUSTOMER.id).to_json())


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds a new group."""

    if (parent := request.json.pop('parent', None)) is not None:
        parent = get_group(parent, CUSTOMER.id)

    group = Group.from_json(request.json, CUSTOMER.id, parent)
    group.save()
    return JSONMessage('Group added.', id=group.id, status=201)


@authenticated
@authorized('dscms4')
@require_json(dict)
def patch(ident: int) -> JSONMessage:
    """Patches the respective group."""

    group = get_group(ident, CUSTOMER.id)
    group.patch_json(request.json)
    group.save()
    return JSONMessage('Group patched.', status=200)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes the respective group."""

    get_group(ident, CUSTOMER.id).delete_instance()
    return JSONMessage('Group deleted.', status=200)


ROUTES = [
    ('GET', '/group', list_),
    ('GET', '/group/<int:ident>', get),
    ('POST', '/group', add),
    ('PATCH', '/group/<int:ident>', patch),
    ('DELETE', '/group/<int:ident>', delete)
]
