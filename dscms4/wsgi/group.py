"""Group Controllers."""

from peewee import DoesNotExist

from wsgilib import JSON
from his.api.handlers import AuthorizedService

from dscms4.orm.group import Group, GROUP_MEMBERS
from dscms4.messages.group import NoSuchGroup

__all__ = ['ROUTES']


def _get_group(gid):
    """Returns the respective group."""

    try:
        return Group.get((Group.id == gid) & (Group.customer == CUSTOMER.id))
    except DoesNotExist:
        raise NoSuchGroup()


def lst():
    """Lists IDs of groups of the respective customer."""

    return JSON([group.id for group in Group.select().where(
        Group.customer == CUSTOMER.id)])


def get(ident):
    """Returns the respective group."""

    return JSON(_get_group().to_dict())


def add():
    """Adds a new group."""

    group = Group.from_dict(DATA.json, customer=CUSTOMER.id)
    group.save()
    return GroupAdded(id=group.id)


@routed('/group/[id:int]')
class GroupHandler(AuthorizedService):
    """Handles groups."""

    @property
    def groups(self):
        """Yields all groups of the current customer."""
        return Group.select().where(Group.customer == self.customer)

    @property
    @lru_cache(maxsize=1)
    def group(self):
        """Returns the requested group."""
        if self.vars['id'] is None:
            raise NoGroupSpecified()

        try:
            return Group.get(
                (Group.id == self.vars['id'])
                & (Group.customer == self.customer))
        except DoesNotExist:
            raise NoSuchGroup() from None

    def get(self):
        """Lists a specific group or all groups if no group is specified."""
        if self.vars['id'] is None:
            if self.query.get('tree', False):
                return JSON(Group.tree_for(self.customer))

            return JSON([group.to_dict() for group in self.groups])

        return JSON(self.group.to_dict())

    def post(self):
        """Adds a new group."""
        group = Group.from_dict(self.data.json, customer=self.customer)
        group.save()
        return GroupAdded(id=group.id)


@routed('/group/<group_id:int>/<type>/[id:int]')
class GroupMemberHandler(AuthorizedService):
    """Handles groups."""

    @property
    @lru_cache(maxsize=1)
    def group(self):
        """Returns the requested group."""
        if self.vars['group_id'] is None:
            raise NoGroupSpecified()

        try:
            return Group.get(
                (Group.id == self.vars['group_id'])
                & (Group.customer == self.customer))
        except DoesNotExist:
            raise NoSuchGroup() from None

    @property
    @lru_cache(maxsize=1)
    def model(self):
        """Returns the respective member model."""
        try:
            return GROUP_MEMBERS[self.vars['type']]
        except KeyError:
            raise UnsupportedMemberType() from None

    @property
    def members(self):
        """Yields all members of the respective group of the speficied type."""
        return self.model.select().where(self.model.group == self.group)

    @property
    @lru_cache(maxsize=1)
    def member(self):
        """Returns the requested group member."""
        if self.vars['id'] is None:
            raise NoMemberSpecified()

        try:
            return self.model.get(
                (self.model.id == self.vars['member_id'])
                & (self.model.customer == self.customer))
        except DoesNotExist:
            raise NoSuchMember() from None

    def get(self):
        """Handles GET requests."""
        if self.vars['id'] is None:
            return JSON([member.to_dict() for member in self.members])

        return JSON(self.member.to_dict())

    def post(self):
        """Adds new group members."""
        record = self.model.from_dict(self.data.json, group=self.group)
        record.save()
        return MemberAdded(id=record.id)

    def delete(self):
        """Deletes group members."""
        self.member.delete_instance()
        return MemberDeleted()


ROUTES = (
    ('/group', 'GET', lst),
    ('/group/<int:ident>', 'GET', get),
    ('/group', 'POST', add),
    ('/group/<int:ident>', 'PATCH', patch),
    ('/group/<int:ident>', 'DELETE', delete))
