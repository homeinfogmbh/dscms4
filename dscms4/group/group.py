"""Group Controllers."""

from typing import Union

from flask import request

from cmslib.functions.group import get_group, get_groups
from cmslib.orm.group import Group
from cmslib.presentation.group import Presentation
from his import CUSTOMER, authenticated, authorized, require_json
from wsgilib import JSON, JSONMessage, XML, get_bool


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists IDs of groups of the respective customer."""

    if get_bool('tree'):
        return JSON([
            group.json_tree for group in get_groups().where(Group.parent >> None)
        ])

    return JSON([group.to_json() for group in get_groups()])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the respective group."""

    return JSON( get_group(ident).to_json())


@authenticated
@authorized('dscms4')
def get_presentation(ident: int) -> Union[JSON, XML]:
    """Returns the presentation for the respective group."""

    presentation = Presentation(get_group(ident))

    if get_bool('xml'):
        return XML(presentation.to_dom())

    return JSON(presentation.to_json())



@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds a new group."""

    parent = request.json.pop('parent', None)

    if parent is not None:
        parent = get_group(parent)

    group = Group.from_json(request.json, CUSTOMER.id, parent)
    group.save()
    return JSONMessage('Group added.', id=group.id, status=201)


@authenticated
@authorized('dscms4')
@require_json(dict)
def patch(ident: int) -> JSONMessage:
    """Patches the respective group."""

    group = get_group(ident)
    group.patch_json(request.json)
    group.save()
    return JSONMessage('Group patched.', status=200)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes the respective group."""

    get_group(ident).delete_instance()
    return JSONMessage('Group deleted.', status=200)


ROUTES = [
    ('GET', '/group', list_),
    ('GET', '/group/<int:ident>', get),
    ('GET', '/group/<int:ident>/presentation', get_presentation),
    ('POST', '/group', add),
    ('PATCH', '/group/<int:ident>', patch),
    ('DELETE', '/group/<int:ident>', delete)
]
