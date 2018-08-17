"""ORM model to represent groups."""

from itertools import chain

from peewee import ForeignKeyField, CharField, TextField

from tenements.orm import ApartmentBuilding
from terminallib import Terminal

from his.messages.data import MissingKeyError, InvalidKeys, NotAnInteger

from dscms4.orm.common import DSCMS4Model, CustomerModel
from dscms4.orm.exceptions import UnsupportedMember, CircularReferenceError, \
    InvalidReferenceError, NoSuchMemberTypeError

__all__ = [
    'group_fk',
    'Group',
    'GroupMemberTerminal',
    'GroupMemberApartmentBuilding',
    'GROUP_MEMBERS',
    'MODELS']


def group_fk(backref):
    """Factory to generate a foreign key field to Group
    for group members with the respective backref.
    """

    return ForeignKeyField(
        Group, column_name='group', on_delete='CASCADE', backref=backref)


class MemberProxy:
    """Proxy to tranparently handle a group's members."""

    def __init__(self, group):
        """Sets the respective group."""
        self.group = group

    def __iter__(self):
        """Yields all members of the respective group."""
        return chain(self.group.terminals, self.group.apartment_buildings)

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
    _parent = ForeignKeyField(
        'self', column_name='parent', null=True, backref='children')

    @classmethod
    def toplevel(cls, customer=None):
        """Yields root-level groups."""
        if customer is None:
            return cls.select().where(cls._parent >> None)

        return cls.select().where(
            (cls.customer == customer) & (cls._parent >> None))

    @classmethod
    def from_json(cls, json, customer, **kwargs):
        """Creates a group from a JSON-ish dictionary."""
        parent = json.pop('parent', None)
        record = super().from_json(json, customer, **kwargs)
        record.parent = parent
        return record

    @classmethod
    def tree_for(cls, customer):
        """Returns JSON-ish groups tree for the respective customer."""
        return [group.dict_tree for group in cls.toplevel(customer=customer)]

    @property
    def parent(self):
        """Returns the parent group."""
        return self._parent

    @parent.setter
    def parent(self, parent):
        """Changes the parent reference of the group."""
        if parent is not None:
            parent = self.get_peer(parent)

            if parent == self or parent in self.childrens_children:
                raise CircularReferenceError()

        self._parent = parent

    @property
    def root(self):
        """Determines whether this group is on the root level."""
        return self.parent is None

    @property
    def childrens_children(self):
        """Recursively yields this group's
        children in a depth-first search.
        """
        for child in self.children:
            for childs_child in child.childrens_children:
                yield childs_child

    @property
    def members(self):
        """Returns a group members proxy."""
        return MemberProxy(self)

    def json_tree(self):
        """Returns the tree for this group."""
        json = self.to_json(parent=False)
        json['children'] = [child.json_tree() for child in self.children]
        return json

    def patch_json(self, json, **kwargs):
        """Creates a group from a JSON-ish dictionary."""
        try:
            parent = json.pop('parent')
        except KeyError:
            pass
        else:
            self.parent = parent

        super().patch_json(json, **kwargs)

    def to_json(self, parent=True, **kwargs):
        """Converts the group to a JSON-ish dictionary."""
        json = super().to_json(**kwargs)

        if parent:
            parent = self.parent

            if parent is None:
                json['parent'] = None
            else:
                json['parent'] = parent.id

        return json

    def delete_instance(self, *args, **kwargs):
        """Deletes the respective instance from the group hierarchy
        setting all child's parent reference to this groups parent.
        """
        for child in self.children:
            child.parent = self.parent
            child.save()

        return super().delete_instance(*args, **kwargs)


class GroupMember(DSCMS4Model):
    """An abstract group member model."""

    @classmethod
    def by_group(cls, group):
        """Yields members for the respective group."""
        return cls.select().where(cls.group == group)

    @classmethod
    def add(cls, group, member_id):
        """Creates a group member from the respective JSON-ish dictionary."""
        member_class = cls.member.rel_model

        try:
            member = member_class.get(
                (member_class.id == member_id)
                & (member_class.customer == group.customer))
        except member_class.DoesNotExist:
            raise InvalidReferenceError()

        return cls(group=group, member=member)

    @staticmethod
    def from_json(json, group, **_):
        """Creates a member for the given group
        from the respective JSON-ish dictionary.
        """
        try:
            member_type = json.pop('type')
        except KeyError:
            raise MissingKeyError('type')

        try:
            member_id = json.pop('id')
        except KeyError:
            raise MissingKeyError('id')

        try:
            member_id = int(member_id)
        except (TypeError, ValueError):
            raise NotAnInteger(member_id)

        if json:
            raise InvalidKeys(keys=tuple(json.keys()))

        try:
            member_class = GROUP_MEMBERS[member_type]
        except KeyError:
            raise NoSuchMemberTypeError()

        return member_class.add(group, member_id)


class GroupMemberTerminal(GroupMember):
    """Terminals as members in groups."""

    class Meta:
        """Meta information for the database model."""
        table_name = 'group_member_terminal'

    group = group_fk('terminals')
    member = ForeignKeyField(
        Terminal, column_name='terminal', on_delete='CASCADE')


class GroupMemberApartmentBuilding(GroupMember):
    """Apartment buildings as members in groups."""

    class Meta:
        """Meta information for the database model."""
        table_name = 'group_member_apartment_building'

    group = group_fk('apartment_buildings')
    member = ForeignKeyField(
        ApartmentBuilding, column_name='apartment_building',
        on_delete='CASCADE')


GROUP_MEMBERS = {
    'terminal': GroupMemberTerminal,
    'building': GroupMemberApartmentBuilding}

MODELS = (Group, GroupMemberTerminal, GroupMemberApartmentBuilding)
