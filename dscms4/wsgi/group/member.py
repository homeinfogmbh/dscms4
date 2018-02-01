"""Group member controllers."""

from his import DATA, authenticated, authorized
from wsgilib import JSON

from dscms4.messages.group import NoSuchMemberType, NoSuchMember, MemberAdded,\
    MemberDeleted
from dscms4.orm.group import GROUP_MEMBERS
from dscms4.wsgi.group.group import get_group

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

    group = get_group(group_id)
    members = {
        member_type: [
            member.to_dict() for member in member_class.select().where(
                member_class.group == group)]
        for member_type, member_class in GROUP_MEMBERS.items()}
    return JSON(members)


@authenticated
@authorized('dscms4')
def add(group_id, member_type):
    """Adds the member to the respective group."""

    group = get_group(group_id)
    member_class = get_member_class(member_type)
    member = member_class.from_dict(group, DATA.json)
    member.save()
    return MemberAdded()


@authenticated
@authorized('dscms4')
def delete(group_id, member_type, member_id):
    """Deletes the respective group member."""

    group = get_group(group_id)
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
    ('POST', '/group/<int:group_id>/member/<member_type>', get,
     'add_group_member'),
    ('DELETE', '/group/<int:group_id>/member/<member_type>/<int:member_id>',
     delete, 'delete_group_member'))
