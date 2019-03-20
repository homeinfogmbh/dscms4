"""Terminals as members in groups."""

from cmslib.functions.group import get_group
from cmslib.messages.group import MEMBER_ADDED
from cmslib.messages.group import MEMBER_DELETED
from cmslib.messages.group import NO_SUCH_MEMBER
from cmslib.orm.group import GroupMemberTerminal
from his import JSON_DATA, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(gid):
    """Returns the group's members."""

    terminals = []

    for group_member_terminal in GroupMemberTerminal.select().where(
            GroupMemberTerminal.group == get_group(gid)):
        terminals.append(group_member_terminal.member.to_json())

    return JSON(terminals)


@authenticated
@authorized('dscms4')
def add(gid):
    """Adds the terminal to the respective group."""

    group = get_group(gid)
    group_member_terminal = GroupMemberTerminal.from_json(JSON_DATA, group)
    group_member_terminal.save()
    return MEMBER_ADDED.update(id=group_member_terminal.id)


@authenticated
@authorized('dscms4')
def delete(gid, member_id):
    """Deletes the respective terminal from the group."""

    try:
        group_member_terminal = GroupMemberTerminal.get(
            (GroupMemberTerminal.group == get_group(gid))
            & (GroupMemberTerminal.id == member_id))
    except GroupMemberTerminal.DoesNotExist:
        raise NO_SUCH_MEMBER

    group_member_terminal.delete_instance()
    return MEMBER_DELETED


ROUTES = (
    ('GET', '/group/<int:gid>/terminal', get, 'get_group_members'),
    ('POST', '/group/<int:gid>/terminal', add, 'add_group_member'),
    ('DELETE', '/group/<int:gid>/terminal/<int:member_id>',
     delete, 'delete_group_member'))
