"""Group Controllers."""

from flask import request

from his import CUSTOMER, JSON_DATA, authenticated, authorized
from wsgilib import JSON

from dscms4.messages.group import GroupAdded, GroupPatched, GroupDeleted
from dscms4.orm.group import Group
from dscms4.wsgi.group.common import get_group


__all__ = ['ROUTES', 'get_group']


@authenticated
@authorized('dscms4')
def list_():
    """Lists IDs of groups of the respective customer."""

    if 'tree' in request.args:
        return JSON([group.json_tree for group in Group.select().where(
            (Group.customer == CUSTOMER.id) & (Group.parent >> None))])

    return JSON([group.to_json() for group in Group.select().where(
        Group.customer == CUSTOMER.id)])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective group."""

    group = get_group(ident)
    return JSON(group.to_json())


@authenticated
@authorized('dscms4')
def add():
    """Adds a new group."""

    group = Group.from_json(JSON_DATA)
    group.save()
    return GroupAdded(id=group.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches the respective group."""

    group = get_group(ident)
    group.patch_json(JSON_DATA)
    group.save()
    return GroupPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes the respective group."""

    group = get_group(ident)
    group.delete_instance()
    return GroupDeleted()


ROUTES = (
    ('GET', '/group', list_, 'list_groups'),
    ('GET', '/group/<int:ident>', get, 'get_group'),
    ('POST', '/group', add, 'add_group'),
    ('PATCH', '/group/<int:ident>', patch, 'patch_group'),
    ('DELETE', '/group/<int:ident>', delete, 'delete_group'))
