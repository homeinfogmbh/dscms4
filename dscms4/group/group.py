"""Group Controllers."""

from flask import request

from cmslib.exceptions import AmbiguousConfigurationsError
from cmslib.exceptions import NoConfigurationFound
from cmslib.functions.group import get_group
from cmslib.messages.group import GROUP_ADDED
from cmslib.messages.group import GROUP_DELETED
from cmslib.messages.group import GROUP_PATCHED
from cmslib.messages.presentation import NO_CONFIGURATION_ASSIGNED
from cmslib.messages.presentation import AMBIGUOUS_CONFIGURATIONS
from cmslib.orm.group import Group
from cmslib.presentation.group import Presentation
from his import CUSTOMER, JSON_DATA, authenticated, authorized
from wsgilib import JSON, XML


__all__ = ['ROUTES']


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
        return AMBIGUOUS_CONFIGURATIONS
    except NoConfigurationFound:
        return NO_CONFIGURATION_ASSIGNED

    return XML(presentation_dom)


@authenticated
@authorized('dscms4')
def add():
    """Adds a new group."""

    group = Group.from_json(JSON_DATA)
    group.save()
    return GROUP_ADDED.update(id=group.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches the respective group."""

    group = get_group(ident)
    group.patch_json(JSON_DATA)
    group.save()
    return GROUP_PATCHED


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes the respective group."""

    group = get_group(ident)
    group.delete_instance()
    return GROUP_DELETED


ROUTES = (
    ('GET', '/group', list_),
    ('GET', '/group/<int:ident>', get),
    ('GET', '/group/<int:ident>/presentation', get_presentation),
    ('POST', '/group', add),
    ('PATCH', '/group/<int:ident>', patch),
    ('DELETE', '/group/<int:ident>', delete)
)
