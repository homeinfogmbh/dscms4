"""Group Controllers."""

from flask import request

from his import CUSTOMER, JSON_DATA, authenticated, authorized
from wsgilib import JSON

from dscms4.messages.group import GroupAdded
from dscms4.messages.group import GroupDeleted
from dscms4.messages.group import GroupPatched
from dscms4.messages.group import NoSuchGroup
from dscms4.orm.group import Group
from dscms4.wsgi.group.tree import get_groups_tree, GroupContent


__all__ = ['ROUTES', 'get_group']


def get_group(ident):
    """Returns the respective group of the current customer."""

    try:
        return Group.get((Group.customer == CUSTOMER.id) & (Group.id == ident))
    except Group.DoesNotExist:
        raise NoSuchGroup()


@authenticated
@authorized('dscms4')
def list_():
    """Lists IDs of groups of the respective customer."""

    if 'assoc' in request.args:
        return JSON([group.to_json() for group in get_groups_tree()])

    return JSON([group.to_json() for group in Group.select().where(
        Group.customer == CUSTOMER.id)])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective group."""

    group = get_group(ident)

    if 'assoc' in request.args:
        group_content = GroupContent(group)
        return JSON(group_content.to_json(recursive=False))

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
