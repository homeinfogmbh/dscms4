"""Group Controllers."""

from flask import request

from his import CUSTOMER, JSON_DATA, authenticated, authorized
from wsgilib import JSON, XML

from cmslib.exceptions import AmbiguousConfigurationsError
from cmslib.exceptions import NoConfigurationFound
from cmslib.messages.group import GroupAdded
from cmslib.messages.group import GroupDeleted
from cmslib.messages.group import GroupPatched
from cmslib.messages.group import NoSuchGroup
from cmslib.messages.presentation import NoConfigurationAssigned
from cmslib.messages.presentation import AmbiguousConfigurations
from cmslib.orm.group import Group
from cmslib.presentation.group import Presentation


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
def get_presentation(ident):
    """Returns the presentation for the respective group."""

    group = get_group(ident)
    presentation = Presentation(group)

    try:
        request.args['xml']
    except KeyError:
        return JSON(presentation.to_json())

    try:
        presentation_dom = presentation.to_dom()
    except AmbiguousConfigurationsError:
        return AmbiguousConfigurations()
    except NoConfigurationFound:
        return NoConfigurationAssigned()

    return XML(presentation_dom)


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
    ('GET', '/group/<int:ident>/presentation', get_presentation,
     'get_group_presentation'),
    ('POST', '/group', add, 'add_group'),
    ('PATCH', '/group/<int:ident>', patch, 'patch_group'),
    ('DELETE', '/group/<int:ident>', delete, 'delete_group'))
