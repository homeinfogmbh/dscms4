"""ORM model to represent groups."""

from peewee import Model, ForeignKeyField, CharField, TextField

from .common import CustomerModel

__all__ = ['Group']


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
            yield from child.tree

    @property
    def members(self):
        """Returns a group members proxy."""
        return MemberProxy(self)

    def to_dict(self):
        """Converts the group to a JSON-like dictionary."""
        return {
            'id': self.id,
            'customer': self.customer.id,
            'name': self.name,
            'description': self.description}
