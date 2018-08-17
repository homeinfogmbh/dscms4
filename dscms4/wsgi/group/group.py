"""Group Controllers."""

from flask import request

from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON

from dscms4.messages.common import CircularReference
from dscms4.messages.group import NoSuchGroup, GroupAdded, GroupPatched, \
    GroupDeleted
from dscms4.orm.exceptions import CircularReferenceError
from dscms4.orm.group import Group

__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_():
    """Lists IDs of groups of the respective customer."""

    return JSON([group.to_json() for group in Group.select().where(
        Group.customer == CUSTOMER.id)])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective group."""

    try:
        group = Group.get(Group.id == ident)
    except Group.DoesNotExist:
        return NoSuchGroup()

    return JSON(group.to_json())


@authenticated
@authorized('dscms4')
def add():
    """Adds a new group."""

    group = Group.from_json(request.json)
    group.save()
    return GroupAdded(id=group.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches the respective group."""

    try:
        group = Group.get(Group.id == ident)
    except Group.DoesNotExist:
        return NoSuchGroup()

    try:
        group.patch_json(request.json)
    except CircularReferenceError:
        return CircularReference()

    group.save()
    return GroupPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes the respective group."""

    try:
        group = Group.get(Group.id == ident)
    except Group.DoesNotExist:
        return NoSuchGroup()

    group.delete_instance()
    return GroupDeleted()


ROUTES = (
    ('GET', '/group', list_, 'list_groups'),
    ('GET', '/group/<int:ident>', get, 'get_group'),
    ('POST', '/group', add, 'add_group'),
    ('PATCH', '/group/<int:ident>', patch, 'patch_group'),
    ('DELETE', '/group/<int:ident>', delete, 'delete_group'))
