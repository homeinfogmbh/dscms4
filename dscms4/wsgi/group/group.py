"""Group Controllers."""

from his import CUSTOMER, DATA, authenticated, authorized
from wsgilib import JSON

from dscms4.messages.common import CircularReference
from dscms4.messages.group import NoSuchGroup, GroupAdded, GroupPatched, \
    GroupDeleted
from dscms4.orm.exceptions import CircularReferenceError
from dscms4.orm.group import KEEP_PARENT, Group

__all__ = ['get_group', 'ROUTES']


def get_group(gid):
    """Returns the respective group of the current customer."""

    try:
        return Group.get((Group.id == gid) & (Group.customer == CUSTOMER.id))
    except Group.DoesNotExist:
        raise NoSuchGroup()


@authenticated
@authorized('dscms4')
def list_():
    """Lists IDs of groups of the respective customer."""

    return JSON([group.to_dict() for group in Group.select().where(
        Group.customer == CUSTOMER.id)])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective group."""

    return JSON(get_group(ident).to_dict())


@authenticated
@authorized('dscms4')
def add():
    """Adds a new group."""

    group = Group.from_dict(CUSTOMER.id, DATA.json)
    group.save()
    return GroupAdded(id=group.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches the respective group."""

    json = DATA.json

    try:
        parent = json.pop('parent')
    except KeyError:
        parent = KEEP_PARENT
    else:
        if parent is not None:
            parent = get_group(parent)

    try:
        get_group(ident).patch(json, parent=parent).save()
    except CircularReferenceError:
        return CircularReference()

    return GroupPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes the respective group."""

    get_group(ident).delete_instance()
    return GroupDeleted()


ROUTES = (
    ('GET', '/group', list_, 'list_groups'),
    ('GET', '/group/<int:ident>', get, 'get_group'),
    ('POST', '/group', add, 'add_group'),
    ('PATCH', '/group/<int:ident>', patch, 'patch_group'),
    ('DELETE', '/group/<int:ident>', delete, 'delete_group'))
