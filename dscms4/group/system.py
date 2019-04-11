"""Digital signage systems as members in groups."""

from cmslib.functions.group import get_group
from cmslib.messages.group import MEMBER_ADDED
from cmslib.messages.group import MEMBER_DELETED
from cmslib.messages.group import NO_SUCH_MEMBER
from cmslib.orm.group import GroupMemberSystem
from his import JSON_DATA, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(gid):
    """Returns the group's members."""

    systems = []

    for group_member_system in GroupMemberSystem.select().where(
            GroupMemberSystem.group == get_group(gid)):
        systems.append(group_member_system.system.id)

    return JSON(systems)


@authenticated
@authorized('dscms4')
def add(gid):
    """Adds a system to the respective group."""

    group = get_group(gid)
    group_member_system = GroupMemberSystem.from_json(JSON_DATA, group)
    group_member_system.save()
    return MEMBER_ADDED.update(id=group_member_system.member.id)


@authenticated
@authorized('dscms4')
def delete(gid, system):
    """Deletes the respective system from the group."""

    try:
        group_member_system = GroupMemberSystem.get(
            (GroupMemberSystem.group == get_group(gid))
            & (GroupMemberSystem.system == system))
    except GroupMemberSystem.DoesNotExist:
        raise NO_SUCH_MEMBER

    group_member_system.delete_instance()
    return MEMBER_DELETED


ROUTES = (
    ('GET', '/group/<int:gid>/system', get),
    ('POST', '/group/<int:gid>/system', add),
    ('DELETE', '/group/<int:gid>/system/<int:system>', delete)
)
