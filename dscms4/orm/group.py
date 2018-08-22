"""ORM model to represent groups."""

from peewee import ForeignKeyField, CharField, TextField

from his.messages.data import MissingKeyError, InvalidKeys
from tenements.orm import ApartmentBuilding
from terminallib import Terminal

from dscms4.messages.common import CircularReference
from dscms4.messages.group import NoSuchMemberType, NoSuchMember
from dscms4.orm.common import RelatedKeyField, CustomerModel, RelatedModel

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

    return RelatedKeyField(
        Group, column_name='group', on_delete='CASCADE', backref=backref)


class Group(CustomerModel):
    """Groups of 'clients' that can be assigned content."""

    name = CharField(255)
    description = TextField(null=True)
    parent = ForeignKeyField(
        'self', column_name='parent', null=True, backref='children')

    @classmethod
    def from_json(cls, json, **kwargs):
        """Creates a group from a JSON-ish dictionary."""
        parent = json.pop('parent', None)
        record = super().from_json(json, **kwargs)
        record.set_parent(parent)
        return record

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
        """Yields the group's members."""
        for typ, model in GROUP_MEMBERS.items():
            records = model.select().where(model.group == self)
            yield (typ, records)

    def set_parent(self, parent):
        """Changes the parent reference of the group."""
        if parent is not None:
            parent = self.get_peer(parent)

            if parent == self or parent in self.childrens_children:
                raise CircularReference()

        self.parent = parent

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
            self.set_parent(parent)

        super().patch_json(json, **kwargs)

    def to_json(self, parent=True, **kwargs):
        """Converts the group to a JSON-ish dictionary."""
        json = super().to_json(**kwargs)

        if parent:
            if self.parent is None:
                json['parent'] = None
            else:
                json['parent'] = self.parent.id

        return json

    def delete_instance(self, *args, **kwargs):
        """Deletes the respective instance from the group hierarchy
        setting all child's parent reference to this groups parent.
        """
        for child in self.children:
            child.set_parent(self.parent)
            child.save()

        return super().delete_instance(*args, **kwargs)


class GroupMember(RelatedModel):
    """An abstract group member model."""

    @staticmethod
    def from_json(json, group, **_):
        """Creates a member for the given group
        from the respective JSON-ish dictionary.
        """
        try:
            member_type = json.pop('type')
        except KeyError:
            raise MissingKeyError('type')

        # The remaining key/value pairs are record identifiers.
        if not json:
            raise MissingKeyError('<identifiers>')

        try:
            member_mapping_class = GROUP_MEMBERS[member_type]
        except KeyError:
            raise NoSuchMemberType()

        member_class = member_mapping_class.member.rel_model
        # Make sure to filter for the respective customer.
        select = member_class.customer == group.customer
        invalid_keys = set()

        # Add filters for all key/value pairs.
        for key, value in json.items():
            try:
                field = getattr(member_class, key)
            except KeyError:
                invalid_keys.add(key)
            else:
                select &= field == value

        if invalid_keys:
            raise InvalidKeys(keys=invalid_keys)

        try:
            member = member_class.get(select)
        except member_class.DoesNotExist:
            raise NoSuchMember()

        return member_mapping_class(group=group, member=member)


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
    'apartment_building': GroupMemberApartmentBuilding}

MODELS = (Group, GroupMemberTerminal, GroupMemberApartmentBuilding)
