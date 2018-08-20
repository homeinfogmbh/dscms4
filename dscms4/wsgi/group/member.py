"""Group member controllers."""

from flask import request

from his import authenticated, authorized
from wsgilib import JSON

from dscms4.messages.group import NoSuchGroup, NoSuchMemberType, NoSuchMember,\
    MemberAdded, MemberDeleted
from dscms4.orm.group import GROUP_MEMBERS, Group, GroupMember


__all__ = ['ROUTES']


def get_member_class(member_type):
    """Returns the respective member class."""

    try:
        return GROUP_MEMBERS[member_type]
    except KeyError:
        raise NoSuchMemberType()


@authenticated
@authorized('dscms4')
def get(group_id):
    """Returns the group's members."""

    try:
        group = Group.cget(Group.id == group_id)
    except Group.DoesNotExist:
        return NoSuchGroup()

    members = {
        typ: [member.to_json() for member in records]
        for typ, records in group.members}
    return JSON(members)


@authenticated
@authorized('dscms4')
def add(group_id):
    """Adds the member to the respective group."""

    try:
        group = Group.cget(Group.id == group_id)
    except Group.DoesNotExist:
        return NoSuchGroup()

    member = GroupMember.from_json(request.json, group)
    member.save()
    return MemberAdded(id=member.id)


@authenticated
@authorized('dscms4')
def delete(group_id, member_type, member_id):
    """Deletes the respective group member."""

    try:
        group = Group.cget(Group.id == group_id)
    except Group.DoesNotExist:
        return NoSuchGroup()

    member_class = get_member_class(member_type)

    try:
        member = member_class.get(
            (member_class.group == group) & (member_class.id == member_id))
    except member_class.DoesNotExist:
        raise NoSuchMember()

    member.delete_instance()
    return MemberDeleted()


ROUTES = (
    ('GET', '/group/<int:group_id>/member', get, 'get_group_members'),
    ('POST', '/group/<int:group_id>/member', add, 'add_group_member'),
    ('DELETE', '/group/<int:group_id>/member/<member_type>/<int:member_id>',
     delete, 'delete_group_member'))
