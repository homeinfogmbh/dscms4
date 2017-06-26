"""Group models"""

from peewee import DoesNotExist, ForeignKeyField, CharField

from .charts import BaseChart
from .client import Client
from .common import CustomerModel
from .menu import Menu

__all__ = ['Group']


class Group(CustomerModel):
    """Group model"""

    name = CharField(255)
    description = CharField(255, null=True, default=None)
    parent = ForeignKeyField(
        'self', db_column='parent', null=True, default=None)

    @classmethod
    def root_groups(cls):
        """Yields root-level groups"""
        return cls.select().where(cls.parent >> None)

    @classmethod
    def _add(cls, customer, name, description=None, parent=None):
        """Actually adds a new group"""
        record = cls()
        record.customer = customer
        record.name = name
        record.description = description
        record.parent = parent
        record.save()
        return record

    @classmethod
    def add(cls, customer, name, description=None, parent=None):
        """Adds a new group"""
        if parent is None:
            try:
                return cls.get((cls.customer == customer) & (cls.name == name))
            except DoesNotExist:
                return cls._add(
                    customer, name, description=description, parent=parent)
        else:
            try:
                return cls.get(
                    (cls.customer == customer) &
                    (cls.name == name) &
                    (cls.parent == parent))
            except DoesNotExist:
                return cls._add(
                    customer, name, description=description, parent=parent)

    def add_client(self, client):
        """Adds a client to the group"""
        return ClientGroup.add(self, client)

    def remove_client(self, client):
        """Removes a client from the group"""
        return ClientGroup.remove(self, client)

    def add_chart(self, chart):
        """Adds a chart to the group"""
        return ChartGroup.add(self, chart)

    def remove_chart(self, chart):
        """Removes a chart from the group"""
        return ChartGroup.remove(self, chart)

    def add_menu(self, menu):
        """Adds a menu to the group"""
        return MenuGroup.add(self, menu)

    def remove_menu(self, menu):
        """Removes a menu from the group"""
        return MenuGroup.remove(self, menu)

    def add_ticker(self, ticker):
        """Adds a ticker to the group"""
        return TickerGroup.add(self, ticker)

    def remove_ticker(self, ticker):
        """Removes a ticker from the group"""
        return TickerGroup.remove(self, ticker)


class ClientGroup(CustomerModel):
    """Client members in groups"""

    group = ForeignKeyField(Group, db_column='group')
    client = ForeignKeyField(Client, db_column='client')

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
    chart = ForeignKeyField(BaseChart, db_column='chart')

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
    menu = ForeignKeyField(Menu, db_column='menu')

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
    ticker = ForeignKeyField(Ticker, db_column='menu')

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
