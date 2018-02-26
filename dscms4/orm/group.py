"""ORM model to represent groups."""

from itertools import chain

from his.messages.data import MissingData, InvalidData
from peewee import ForeignKeyField, CharField, TextField

from tenements.orm import ApartmentBuilding
from terminallib import Terminal

from dscms4.orm.common import DSCMS4Model, CustomerModel
from dscms4.orm.exceptions import UnsupportedMember, CircularPedigreeError, \
    NoSuchTerminal, NoSuchApartment

__all__ = [
    'KEEP_PARENT',
    'Group',
    'GroupMemberTerminal',
    'GroupMemberApartmentBuilding',
    'GROUP_MEMBERS',
    'MODELS']


KEEP_PARENT = object()


class MemberProxy:
    """Proxy to tranparently handle a group's members."""

    def __init__(self, group):
        """Sets the respective group."""
        self.group = group

    def __iter__(self):
        """Yields all members of the respective group."""
        return chain(self.terminals, self.apartment_buildings)

    @property
    def terminals(self):
        """Yields terminals."""
        for mapping in GroupMemberTerminal.select().where(
                GroupMemberTerminal.group == self.group):
            yield mapping.terminal

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
        elif isinstance(member, ApartmentBuilding):
            member = GroupMemberApartmentBuilding.add(self.group, member)
        else:
            raise UnsupportedMember(member)

        member.save()
        return member

    def remove(self, member):
        """Removes the respective member from the group."""
        if isinstance(member, Terminal):
            for mapping in GroupMemberTerminal.select().where(
                    (GroupMemberTerminal.group == self.group) &
                    (GroupMemberTerminal.terminal == member)):
                mapping.delete_instance()
        elif isinstance(member, ApartmentBuilding):
            for mapping in GroupMemberApartmentBuilding.select().where(
                    (GroupMemberApartmentBuilding.group == self.group) &
                    (GroupMemberApartmentBuilding.tenement == member)):
                mapping.delete_instance()


class Group(CustomerModel):
    """Groups of 'clients' that can be assigned content."""

    name = CharField(255)
    description = TextField(null=True)
    parent = ForeignKeyField('self', column_name='parent', null=True)

    @classmethod
    def toplevel(cls, customer=None):
        """Yields root-level groups."""
        if customer is None:
            return cls.select().where(cls.parent >> None)

        return cls.select().where(
            (cls.customer == customer) & (cls.parent >> None))

    @classmethod
    def from_dict(cls, customer, dictionary, **kwargs):
        """Creates a group from the respective dictionary."""
        parent = dictionary.pop('parent', None)
        record = super().from_dict(customer, dictionary, **kwargs)
        record.change_parent(parent)
        return record

    @classmethod
    def tree_for(cls, customer):
        """Returns JSON-ish groups tree for the respective customer."""
        return [group.dict_tree for group in cls.toplevel(customer=customer)]

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
    def dict_tree(self):
        """Returns the tree for this group."""
        dictionary = self.to_dict(parent=False)
        dictionary['children'] = [group.dict_tree for group in self.children]
        return dictionary

    @property
    def members(self):
        """Returns a group members proxy."""
        return MemberProxy(self)

    def patch(self, dictionary, parent=KEEP_PARENT, **kwargs):
        """Creates a group from the respective dictionary."""
        super().patch(dictionary, **kwargs)

        if parent is not KEEP_PARENT:
            self.change_parent(parent)

        return self

    def change_parent(self, parent):
        """Changes the parent reference of the group."""
        if parent is not None and parent in self.tree:
            raise CircularPedigreeError()

        self.parent = parent

    def to_dict(self, parent=True, **kwargs):
        """Converts the group to a JSON-like dictionary."""
        dictionary = super().to_dict(**kwargs)

        if parent:
            if self.parent is None:
                dictionary['parent'] = None
            else:
                dictionary['parent'] = self.parent.id

        return dictionary


class GroupMember(DSCMS4Model):
    """An abstract group member model."""

    group = ForeignKeyField(Group, column_name='group', on_delete='CASCADE')

    @classmethod
    def by_group(cls, group):
        """Yields members for the respective group."""
        return cls.select().where(cls.group == group)

    def to_dict(self, *args, **kwargs):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_dict(*args, **kwargs)
        dictionary['gid'] = self.group.id
        return dictionary


class GroupMemberTerminal(GroupMember):
    """Terminals as members in groups."""

    class Meta:
        """Meta information for the database model."""
        table_name = 'group_member_terminal'

    terminal = ForeignKeyField(
        Terminal, column_name='terminal', on_delete='CASCADE')

    @classmethod
    def add(cls, group, terminal):
        """Adds a new record."""
        record = cls()
        record.group = group
        record.terminal = terminal
        return record

    @classmethod
    def from_dict(cls, group, dictionary):
        """Creates a new record from the provided dictionary."""
        try:
            tid = int(dictionary['tid'])
        except (KeyError, TypeError):
            raise MissingData('tid')
        except ValueError:
            raise InvalidData('tid')

        try:
            terminal = Terminal.get(
                (Terminal.customer == group.customer) & (Terminal.tid == tid))
        except Terminal.DoesNotExist:
            raise NoSuchTerminal()

        return cls.add(group, terminal)

    def to_dict(self, *args, **kwargs):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_dict(*args, **kwargs)
        dictionary['tid'] = self.terminal.id
        return dictionary


class GroupMemberApartmentBuilding(GroupMember):
    """Apartment buildings as members in groups."""

    class Meta:
        """Meta information for the database model."""
        table_name = 'group_member_apartment_building'

    apartment_building = ApartmentBuilding(
        Terminal, column_name='apartment_building', on_delete='CASCADE')

    @classmethod
    def add(cls, group, apartment_building):
        """Adds a new record."""
        record = cls()
        record.group = group
        record.apartment_building = apartment_building
        return record

    @classmethod
    def from_dict(cls, group, dictionary):
        """Creates a new record from the provided dictionary."""
        try:
            ident = int(dictionary['id'])
        except (KeyError, TypeError):
            raise MissingData('id')
        except ValueError:
            raise InvalidData('id')

        try:
            apartment_building = ApartmentBuilding.get(
                (ApartmentBuilding.customer == group.customer)
                & (ApartmentBuilding.id == ident))
        except ApartmentBuilding.DoesNotExist:
            raise NoSuchApartment()

        return cls.add(group, apartment_building)


GROUP_MEMBERS = {
    'terminal': GroupMemberTerminal,
    'building': GroupMemberApartmentBuilding}

MODELS = (Group, GroupMemberTerminal, GroupMemberApartmentBuilding)
