"""Group models"""

from contextlib import suppress
from peewee import DoesNotExist, ForeignKeyField, CharField

from .common import CustomerModel

__all__ = ['Group', 'Member']


class MembersProxy():
    """Proxy to retrieve a group's members"""

    def __init__(self, group):
        self.group = group

    def __iter__(self):
        """Yields all types of members"""
        yield from GroupMember

    def add(self, member):
        """Adds a new member"""
        return GroupMember.add(self.group, member)

    def remove(self, member, all=False):
        """Removes a member from the group"""
        if all:
            for group_member in GroupMember.select().where(
                    (GroupMember.group == self.group) &
                    (GroupMember.member == member)):
                group_member.delete_instance()
        else:
            try:
                group_member = GroupMember.get(
                    (GroupMember.group == self.group) &
                    (GroupMember.member == member))
            except DoesNotExist:
                pass
            else:
                group_member.delete_instance()


class Group(CustomerModel):
    """Group model"""

    name = CharField(255)
    description = CharField(255, null=True, default=None)
    parent = ForeignKeyField(
        'self', db_column='parent', null=True, default=None)

    @classmethod
    def toplevel(cls):
        """Yields top-level groups"""
        return cls.select().where(cls.parent >> None)

    @classmethod
    def _add(cls, customer, name, description=None, parent=None):
        """Actually creates a new group"""
        record = cls()
        record.customer = customer
        record.name = name
        record.description = description
        record.parent = parent
        record.save()
        return record

    @classmethod
    def add(cls, customer, name, description=None, parent=None):
        """Creates a new group iff not yet existing"""
        if parent is None:
            with suppress(DoesNotExist):
                return cls.get((cls.customer == customer) & (cls.name == name))
        else:
            with suppress(DoesNotExist):
                return cls.get(
                    (cls.customer == customer) &
                    (cls.name == name) &
                    (cls.parent == parent))

        return cls._create(
            customer, name, description=description, parent=parent)

    @property
    def children(self):
        """Yields groups that have this group as parent"""
        return self.__class__.select().where(self.__class__.parent == self)

    @property
    def members(self):
        """Returns a members proxy"""
        return MembersProxy(self)

    def to_dict(self, cascade=False):
        """Converts the group to a JSON-like dictionary"""
        if not cascade:
            return {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'parent': self.parent.id}
        else:
            return {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'children': [
                    child.to_dict(cascade=cascade) for child in self.children],
                'members': [member.to_dict() for member in self.members]}


class Member(CustomerModel):
    """A group member"""

    @classmethod
    def add(cls):
        """Adds a new member"""
        member = cls()
        member.save()
        return member

    @property
    def groups(self):
        """Yields groups this member is in"""
        for group_member in GroupMember.select().where(
                GroupMember.member == self):
            yield group_member.group

    def join(self, group):
        """Joins a group"""
        return GroupMember.add(group, self)

    def leave(self, group):
        """Leaves a group"""
        return GroupMember.remove(group, self)

    def leave_all(self):
        """Leaves all groups"""
        for group_member in GroupMember.select().where(
                GroupMember.member == self):
            group_member.delete_instance()

    def remove(self):
        """Leaves all groups and deletes instance"""
        self.leave_all()
        self.delete_instance()


class GroupMember(CustomerModel):
    """Mapping between groups and members"""

    class Meta:
        db_table = 'group_member'

    group = ForeignKeyField(Group, db_column='group')
    member = ForeignKeyField(Member, db_column='member')

    @classmethod
    def add(cls, group, member):
        """Adds the member to the group"""
        try:
            return cls.get((cls.group == group) & (cls.member == member))
        except DoesNotExist:
            record = cls()
            record.group = group
            record.member = member
            record.save()
            return record

    @classmethod
    def remove(cls, group, member):
        """Removes the member from the group"""
        for record in cls.select().where(
                (cls.group == group) & (cls.member == member)):
            record.delete_instance()
