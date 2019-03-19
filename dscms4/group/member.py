"""Group member controllers."""

from cmslib.functions.group import get_group
from cmslib.messages.group import MEMBER_ADDED
from cmslib.messages.group import MEMBER_DELETED
from cmslib.messages.group import NO_SUCH_MEMBER
from cmslib.messages.group import NO_SUCH_MEMBER_TYPE
from cmslib.orm.group import GROUP_MEMBERS, GroupMember
from his import JSON_DATA, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


def get_member_class(member_type):
    """Returns the respective member class."""

    try:
        return GROUP_MEMBERS[member_type]
    except KeyError:
        raise NO_SUCH_MEMBER_TYPE


@authenticated
@authorized('dscms4')
def get(gid):
    """Returns the group's members."""

    group = get_group(gid)
    members = {
        typ: [member.to_json() for member in records]
        for typ, records in group.members}
    return JSON(members)


@authenticated
@authorized('dscms4')
def add(gid):
    """Adds the member to the respective group."""

    group = get_group(gid)
    member = GroupMember.from_json(JSON_DATA, group)
    member.save()
    return MEMBER_ADDED.update(id=member.id)


@authenticated
@authorized('dscms4')
def delete(gid, member_type, member_id):
    """Deletes the respective group member."""

    group = get_group(gid)
    member_class = get_member_class(member_type)

    try:
        member = member_class.get(
            (member_class.group == group) & (member_class.id == member_id))
    except member_class.DoesNotExist:
        raise NO_SUCH_MEMBER

    member.delete_instance()
    return MEMBER_DELETED


ROUTES = (
    ('GET', '/group/<int:gid>/member', get, 'get_group_members'),
    ('POST', '/group/<int:gid>/member', add, 'add_group_member'),
    ('DELETE', '/group/<int:gid>/member/<member_type>/<int:member_id>',
     delete, 'delete_group_member'))
