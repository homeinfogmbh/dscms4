"""Company structure"""

from peewee import DoesNotExist, ForeignKeyField, CharField, SmallIntegerField
from homeinfo.crm import Address, Customer

from .common import DSCMS4Model
from .charts import BaseChart
from .menu import Menu
from .configuration import Configuration
from .ticker import Ticker
from .presentation import GroupChart, BuildingChart, RentalUnitChart, \
    GroupMenu, BuildingMenu, RentalUnitMenu, \
    GroupConfiguration, BuildingConfiguration, RentalUnitConfiguration, \
    GroupTicker, BuildingTicker, RentalUnitTicker


class InvalidItem(Exception):
    """Indicates that an assignment of
    an invalid item was attempted
    """

    pass


class Building(DSCMS4Model):
    """An organizational unit"""

    customer = ForeignKeyField(Customer, db_column='customer')
    address = ForeignKeyField(Address, db_column='address')
    name = CharField(255, null=True, default=None)
    description = CharField(255, null=True, default=None)

    def assign(self, item):
        """Assigns an item (Chart, Ticker, etc.) to the rental unit"""
        if isinstance(item, BaseChart):
            BuildingChart.add(item)
        elif isinstance(item, Ticker):
            BuildingTicker.add(item)
        elif isinstance(item, Menu):
            BuildingMenu.add(item)
        elif isinstance(item, Configuration):
            BuildingConfiguration.add(item)
        else:
            raise InvalidItem()

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = {'address': self.address.to_dict()}

        if self.name is not None:
            dictionary['name'] = self.name

        if self.description is not None:
            dictionary['description'] = self.description

        return dictionary


class RentalUnit(DSCMS4Model):
    """A rental unit"""

    class Meta:
        db_table = 'rental_unit'

    building = ForeignKeyField(Building, db_column='building')
    ident = CharField(255)
    floor = SmallIntegerField(null=True, default=None)
    orientation = CharField(255, null=True, default=None)

    def assign(self, item):
        """Assigns an item (Chart, Ticker, etc.) to the rental unit"""
        if isinstance(item, BaseChart):
            RentalUnitChart.add(item)
        elif isinstance(item, Ticker):
            RentalUnitTicker.add(item)
        elif isinstance(item, Menu):
            RentalUnitMenu.add(item)
        elif isinstance(item, Configuration):
            RentalUnitConfiguration.add(item)
        else:
            raise InvalidItem()

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = {'ident': self.ident}

        if self.floor is not None:
            dictionary['floor'] = self.floor

        if self.orientation is not None:
            dictionary['orientation'] = self.orientation

        return dictionary


class Group(DSCMS4Model):
    """Organizational container for rental
    units, Buildings and other groups
    """

    customer = ForeignKeyField(Customer, db_column='customer')
    name = CharField(255)
    description = CharField(255, null=True, default=None)

    def add(self, member):
        """Adds a member to a group"""
        if isinstance(member, Building):
            try:
                return BuildingMember.get(
                    (BuildingMember.group == self) &
                    (BuildingMember.member == member))
            except DoesNotExist:
                building_member = BuildingMember()
                building_member.group = self
                building_member.member = member
                building_member.save()
                return building_member
        elif isinstance(member, RentalUnit):
            try:
                return RentalUnitMember.get(
                    (RentalUnitMember.group == self) &
                    (RentalUnitMember.member == member))
            except DoesNotExist:
                rental_unit_member = RentalUnitMember()
                rental_unit_member.group = self
                rental_unit_member.member = member
                rental_unit_member.save()
                return rental_unit_member
        elif isinstance(member, Group):
            try:
                return GroupMember.get(
                    (GroupMember.group == self) &
                    (GroupMember.member == member))
            except DoesNotExist:
                if member == self:
                    raise ValueError('Cannot add a group to itself')
                else:
                    group_member = GroupMember()
                    group_member.group = self
                    group_member.member = member
                    group_member.save()
                    return group_member
        else:
            raise ValueError('Invalid member: {}'.format(member))

    def members(self, typ=None):
        """Yields all members of the group"""
        if typ is None or typ is Building:
            for building_member in BuildingMember.select().where(
                    BuildingMember.group == self):
                yield building_member.member

        if typ is None or typ is RentalUnit:
            for rental_unit_member in RentalUnitMember.select().where(
                    RentalUnitMember.group == self):
                yield rental_unit_member.member

        if typ is None or typ is Group:
            for group_member in GroupMember.select().where(
                    GroupMember.group == self):
                yield group_member.member

    def assign(self, item):
        """Assigns an item (Chart, Ticker, etc.) to the group"""
        if isinstance(item, BaseChart):
            GroupChart.add(item)
        elif isinstance(item, Ticker):
            GroupTicker.add(item)
        elif isinstance(item, Menu):
            GroupMenu.add(item)
        elif isinstance(item, Configuration):
            GroupConfiguration.add(item)
        else:
            raise InvalidItem()

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = {'name': self.name}

        if self.description is not None:
            dictionary['description'] = self.description

        members = [member.to_dict() for member in self.members()]

        if members:
            dictionary['members'] = members

        return dictionary


class _GroupMember(DSCMS4Model):
    """Members of groups"""

    group = ForeignKeyField(Group, db_column='group')


class BuildingMember(_GroupMember):
    """Building members"""

    class Meta:
        db_table = 'building_member'

    member = ForeignKeyField(Building, db_column='member')


class RentalUnitMember(_GroupMember):
    """Rental unit members"""

    class Meta:
        db_table = 'rental_unit_member'

    member = ForeignKeyField(RentalUnit, db_column='member')


class GroupMember(_GroupMember):
    """Groups within groups members"""

    class Meta:
        db_table = 'group_member'

    member = ForeignKeyField(Group, db_column='member')
