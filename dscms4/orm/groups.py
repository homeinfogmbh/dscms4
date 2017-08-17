"""Group models"""

from contextlib import suppress
from peewee import DoesNotExist, ForeignKeyField, CharField

from .charts import BaseChart
from .client import Client
from .common import CustomerModel
from .menu import Menu
from .ticker import Ticker

__all__ = ['Group']


class GroupProxy():
    """Common, abstract group proxy"""

    def __init__(self, group):
        self.group = group


class MemberProxy(GroupProxy):
    """Proxies members"""

    def __init__(self, group, mapping):
        super().__init__(group)
        self.mapping = mapping

    def __iter__(self):
        """Yields the members from the repsective mapping"""
        for mapping in self.mapping.select().where(
                self.mapping.group == self.group):
            yield mapping.member

    def add(self, member):
        """Adds a new member"""
        return self.mapping.add(self.group, member)

    def remove(self, member, all=False):
        """Removes a member from the group"""
        if all:
            for mapping in self.mapping.select().where(
                    (self.mapping.group == self.group) &
                    (self.mapping.member == member)):
                mapping.delete_instance()
        else:
            try:
                mapping = self.mapping.get(
                    (self.mapping.group == self.group) &
                    (self.mapping.member == member))
            except DoesNotExist:
                pass
            else:
                mapping.delete_instance()


class MembersProxy(GroupProxy):
    """Proxy to retrieve a group's members"""

    def __iter__(self):
        """Yields all types of members"""
        yield from self.clients
        yield from self.charts
        yield from self.menus
        yield from self.tickers

    @property
    def clients(self):
        """Yields client members of the group"""
        return MemberProxy(self.group, ClientGroup)

    @property
    def charts(self):
        """Yields chart members of the group"""
        return MemberProxy(self.group, ChartGroup)

    @property
    def menus(self):
        """Yields menu members of the group"""
        return MemberProxy(self.group, MenuGroup)

    @property
    def tickers(self):
        """Yields ticker members of the group"""
        return MemberProxy(self.group, TickerGroup)


class AppendProxy(GroupProxy):
    """Proxy to add different types of
    members to the respective group
    """

    def client(self, client):
        """Adds a client to the group"""
        return ClientGroup.add(self.group, client)

    def chart(self, chart):
        """Adds a chart to the group"""
        return ChartGroup.add(self.group, chart)

    def menu(self, menu):
        """Adds a menu to the group"""
        return MenuGroup.add(self.group, menu)

    def ticker(self, ticker):
        """Adds a ticker to the group"""
        return TickerGroup.add(self.group, ticker)


class RemoveProxy(GroupProxy):
    """Proxy to remove different types of
    members to the respective group"""

    def client(self, client):
        """Removes a client from the group"""
        return ClientGroup.remove(self.group, client)

    def chart(self, chart):
        """Removes a chart from the group"""
        return ChartGroup.remove(self.group, chart)

    def menu(self, menu):
        """Removes a menu from the group"""
        return MenuGroup.remove(self.group, menu)

    def ticker(self, ticker):
        """Removes a ticker from the group"""
        return TickerGroup.remove(self.group, ticker)


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


class ClientGroup(CustomerModel):
    """Client members in groups"""

    group = ForeignKeyField(Group, db_column='group')
    member = client = ForeignKeyField(Client, db_column='client')

    @classmethod
    def add(cls, group, client):
        """Adds the client to the group"""
        try:
            return cls.get((cls.group == group) & (cls.client == client))
        except DoesNotExist:
            record = cls()
            record.group = group
            record.client = client
            record.save()
            return record

    @classmethod
    def remove(cls, group, client):
        """Removes the client from the group"""
        for record in cls.select().where(
                (cls.group == group) & (cls.client == client)):
            # TODO: Delete references beforehand
            record.delete_instance()


class ChartGroup(CustomerModel):
    """Mapping between groups and charts"""

    group = ForeignKeyField(Group, db_column='group')
    member = chart = ForeignKeyField(BaseChart, db_column='chart')

    @classmethod
    def add(cls, group, chart):
        """Adds the chart to the group"""
        try:
            return cls.get((cls.group == group) & (cls.chart == chart))
        except DoesNotExist:
            record = cls()
            record.group = group
            record.chart = chart
            record.save()
            return record

    @classmethod
    def remove(cls, group, chart):
        """Removes the chart from the group"""
        for record in cls.select().where(
                (cls.group == group) & (cls.chart == chart)):
            # TODO: Delete references beforehand
            record.delete_instance()


class MenuGroup(CustomerModel):
    """Menu members in groups"""

    group = ForeignKeyField(Group, db_column='group')
    member = menu = ForeignKeyField(Menu, db_column='menu')

    @classmethod
    def add(cls, group, menu):
        """Adds the menu to the group"""
        try:
            return cls.get((cls.group == group) & (cls.menu == menu))
        except DoesNotExist:
            record = cls()
            record.group = group
            record.menu = menu
            record.save()
            return record

    @classmethod
    def remove(cls, group, menu):
        """Removes the menu from the group"""
        for record in cls.select().where(
                (cls.group == group) & (cls.menu == menu)):
            # TODO: Delete references beforehand
            record.delete_instance()


class TickerGroup(CustomerModel):
    """Ticket members in groups"""

    group = ForeignKeyField(Group, db_column='group')
    member = ticker = ForeignKeyField(Ticker, db_column='ticker')

    @classmethod
    def add(cls, group, ticker):
        """Adds the ticker to the group"""
        try:
            return cls.get((cls.group == group) & (cls.ticker == ticker))
        except DoesNotExist:
            record = cls()
            record.group = group
            record.ticker = ticker
            record.save()
            return record

    @classmethod
    def remove(cls, group, ticker):
        """Removes the ticker from the group"""
        for record in cls.select().where(
                (cls.group == group) & (cls.ticker == ticker)):
            # TODO: Delete references beforehand
            record.delete_instance()
