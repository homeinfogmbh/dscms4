"""ORM model to represent groups."""

from itertools import chain

from peewee import Model, ForeignKeyField, CharField, TextField

from tenements.orm import ApartmentBuilding
from terminallib import Terminal

try:
    from his.comcat import ComCatAccount
except ImportError:
    class ComCatAccount(Model):
        """Mockup."""
        pass

from .common import CustomerModel, DSCMS4Model
from .exceptions import UnsupportedMember, CircularPedigreeError

__all__ = [
    'Group',
    'GroupMemberTerminal',
    'GroupMemberComCatAccount',
    'GroupMemberApartmentBuilding',
    'MODELS']


class MemberProxy:
    """Proxy to tranparently handle a group's members."""

    def __init__(self, group):
        """Sets the respective group."""
        self.group = group

    def __iter__(self):
        """Yields all members of the respective group."""
        return chain(self.terminals, self.comcat_accounts,
                     self.apartment_buildings)

    @property
    def terminals(self):
        """Yields terminals."""
        for mapping in GroupMemberTerminal.select().where(
                GroupMemberTerminal.group == self.group):
            yield mapping.terminal

    @property
    def comcat_accounts(self):
        """Yields ComCat accounts."""
        for mapping in GroupMemberComCatAccount.select().where(
                GroupMemberComCatAccount.group == self.group):
            yield mapping.comcat_account

    @property
    def apartment_buildings(self):
        """Yields apartment buildings."""
        for mapping in GroupMemberApartmentBuilding.select().where(
                GroupMemberApartmentBuilding.group == self.group):
            yield mapping.apartment_building

    def add(self, member):
        """Adds a member to the respective group."""
        if isinstance(member, Terminal):
            member = GroupMemberTerminal.add(self.group, member)
        elif isinstance(member, ComCatAccount):
            member = GroupMemberComCatAccount.add(self.group, member)
        elif isinstance(member, ApartmentBuilding):
            member = GroupMemberApartmentBuilding.add(self.group, member)
        else:
            raise UnsupportedMember(member) from None

        member.save()
        return member

    def remove(self, member):
        """Removes the respective member from the group."""
        if isinstance(member, Terminal):
            for mapping in GroupMemberTerminal.select().where(
                    (GroupMemberTerminal.group == self.group) &
                    (GroupMemberTerminal.terminal == member)):
                mapping.delete_instance()
        elif isinstance(member, ComCatAccount):
            for mapping in GroupMemberComCatAccount.select().where(
                    (GroupMemberComCatAccount.group == self.group) &
                    (GroupMemberComCatAccount.comcat_account == member)):
                mapping.delete_instance()
        elif isinstance(member, ApartmentBuilding):
            for mapping in GroupMemberApartmentBuilding.select().where(
                    (GroupMemberApartmentBuilding.group == self.group) &
                    (GroupMemberApartmentBuilding.tenement == member)):
                mapping.delete_instance()


class Group(Model, CustomerModel):
    """Groups of 'clients' that can be assigned content."""

    name = CharField(255)
    description = TextField(null=True, default=None)
    parent = ForeignKeyField(
        'self', db_column='parent', null=True, default=None)

    @classmethod
    def toplevel(cls):
        """Yields root-level groups."""
        return cls.select().where(cls.parent >> None)

    @classmethod
    def add(cls, customer, name, description=None, parent=None):
        """Adds a new group."""
        record = cls()
        record.customer = customer
        record.name = name
        record.description = description
        record.parent = parent
        record.save()
        return record

    @property
    def root(self):
        """Determines whether this group is on the root level."""
        return self.parent is None

    @property
    def children(self):
        """Yields groups that have this group as parent."""
        return self.__class__.select().where(self.__class__.parent == self)

    @property
    def tree(self):
        """Recursively yields the tree with this group
        as root element in a depth-first search.
        """
        yield self

        for child in self.children:
            for element in child.tree:
                yield element

    @property
    def members(self):
        """Returns a group members proxy."""
        return MemberProxy(self)

    def change_parent(self, parent):
        """Changes the parent reference of the group."""
        if parent in self.tree:
            raise CircularPedigreeError()

        self.parent = parent
        self.save()
        return self

    def to_dict(self):
        """Converts the group to a JSON-like dictionary."""
        return {
            'id': self.id,
            'customer': self.customer.id,
            'name': self.name,
            'description': self.description}


class GroupMember(DSCMS4Model):
    """An abstract group member model."""

    group = ForeignKeyField(Group, db_column='group')

    @classmethod
    def by_group(cls, group):
        """Yields members for the respective group."""
        return cls.select().where(cls.group == group)


class GroupMemberTerminal(Model, GroupMember):
    """Terminals as members in groups."""

    class Meta:
        """Meta information for the database model."""
        db_table = 'group_member_terminal'

    terminal = ForeignKeyField(Terminal, db_column='terminal')

    @classmethod
    def add(cls, group, terminal):
        """Adds a new record."""
        record = cls()
        record.group = group
        record.terminal = terminal
        return record


class GroupMemberComCatAccount(Model, GroupMember):
    """ComCat accounts as members in groups."""

    class Meta:
        """Meta information for the database model."""
        db_table = 'group_member_comcat_account'

    comcat_account = ForeignKeyField(
        ComCatAccount, db_column='comcat_account')

    @classmethod
    def add(cls, group, comcat_account):
        """Adds a new record."""
        record = cls()
        record.group = group
        record.comcat_account = comcat_account
        return record


class GroupMemberApartmentBuilding(Model, GroupMember):
    """Apartment buildings as members in groups."""

    class Meta:
        """Meta information for the database model."""
        db_table = 'group_member_apartment_building'

    apartment_building = ApartmentBuilding(
        Terminal, db_column='apartment_building')

    @classmethod
    def add(cls, group, apartment_building):
        """Adds a new record."""
        record = cls()
        record.group = group
        record.apartment_building = apartment_building
        return record


MODELS = (
    Group, GroupMemberTerminal, GroupMemberComCatAccount,
    GroupMemberApartmentBuilding)
