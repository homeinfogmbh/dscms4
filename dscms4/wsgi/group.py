"""Group Controllers."""

from peewee import DoesNotExist

from his import CUSTOMER, DATA
from wsgilib import JSON

from dscms4.messages.group import NoSuchGroup, NoSuchMemberType, NoSuchMember,\
    GroupAdded, GroupPatched, GroupDeleted, MemberAdded, MemberDeleted
from dscms4.orm.group import Group, GROUP_MEMBERS

__all__ = ['ROUTES']


def _get_group(gid):
    """Returns the respective group."""

    try:
        return Group.get((Group.id == gid) & (Group.customer == CUSTOMER.id))
    except DoesNotExist:
        raise NoSuchGroup()


def _get_member_class(member_type):
    """Returns the respective member class."""

    try:
        return GROUP_MEMBERS[member_type]
    except KeyError:
        raise NoSuchMemberType()


@authenticated
@authorized('dscms4')
def lst():
    """Lists IDs of groups of the respective customer."""

    return JSON([group.id for group in Group.select().where(
        Group.customer == CUSTOMER.id)])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective group."""

    return JSON(_get_group(ident).to_dict())


@authenticated
@authorized('dscms4')
def add():
    """Adds a new group."""

    group = Group.from_dict(DATA.json, customer=CUSTOMER.id)
    group.save()
    return GroupAdded(id=group.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches the respective group."""

    _get_group(ident).patch(DATA.json)
    return GroupPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes the respective group."""

    _get_group(ident).delete_instance()
    return GroupDeleted()


@authenticated
@authorized('dscms4')
def get_members(group_id):
    """Returns the group's members."""

    group = _get_group(group_id)
    members = {
        member_type: [
            member.to_dict() for member in member_class.select().where(
                member_class.group == group)]
        for member_type, member_class in GROUP_MEMBERS.items()}
    return JSON(members)


@authenticated
@authorized('dscms4')
def add_member(group_id, member_type):
    """Adds the member to the respective group."""

    group = _get_group(group_id)
    member_class = _get_member_class(member_type)
    member = member_class.from_dict(group, DATA.json)
    member.save()
    return MemberAdded()


@authenticated
@authorized('dscms4')
def delete_member(group_id, member_type, member_id):
    """Deletes the respective group member."""

    group = _get_group(group_id)
    member_class = _get_member_class(member_type)

    try:
        member = member_class.get(
            (member_class.group == group) & (member_class.id == member_id))
    except DoesNotExist:
        raise NoSuchMember()

    member.delete_instance()
    return MemberDeleted()


ROUTES = (
    ('GET', '/group', lst, 'list_groups'),
    ('GET', '/group/<int:ident>', get, 'get_group'),
    ('POST', '/group', add, 'add_group'),
    ('PATCH', '/group/<int:ident>', patch, 'patch_group'),
    ('DELETE', '/group/<int:ident>', delete, 'delete_group'),
    ('GET', '/group/<int:group_id>/member', get_members, 'get_group_members'),
    ('POST', '/group/<int:group_id>/member/<member_type>', get_members,
     'add_group_member'),
    ('DELETE', '/group/<int:group_id>/member/<member_type>/<int:member_id>',
     delete_member, 'delete_group_member'))
