"""Group models"""

from contextlib import suppress
from peewee import DoesNotExist, ForeignKeyField, CharField

from homeinfo.terminals.orm import Terminal

from .common import CustomerModel

__all__ = ['Group', 'TerminalMember']


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

    def to_dict(self, cascade=False):
        """Converts the group to a JSON-like dictionary"""
        dictionary = {
            'id': self.id,
            'name': self.name,
            'description': self.description}

        if not cascade:
            dictionary['parent'] = self.parent.id
        else:
            dictionary['children'] = [
                child.to_dict(cascade=cascade) for child in self.children]

        return dictionary


class TerminalMember():
    """Mapping between terminal members and groups"""

    group = ForeignKeyField(Group, db_column='group')
    terminal = ForeignKeyField(Terminal, db_column='terminal')

    @classmethod
    def _add(cls, group, terminal):
        """Adds a new member"""
        member = cls()
        member.group = group
        member.terminal = terminal
        member.save()
        return member

    @classmethod
    def add(cls, group, terminal):
        """Adds the member to the group"""
        try:
            return cls.get((cls.group == group) & (cls.terminal == terminal))
        except DoesNotExist:
            return cls._add(group, terminal)
