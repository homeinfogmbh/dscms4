"""ORM models for group membership mapping."""

from peewee import DoesNotExist, Model, ForeignKeyField

from homeinfo.terminals.orm import Terminal
from comcat import ComcatAccount    # TODO: implement
from tenements import Tenement      # TODO: implement

from .common import DSCMS4Model
from .group import Group


__all__ = ['MemberTerminal', 'MemberComcatAccount', 'MemberTenement']


class GroupMember(DSCMS4Model):
    """An abstract group member."""

    group = ForeignKeyField(Group, db_column='group')


class MemberTerminal(Model, GroupMember):
    """Mapping between terminals and groups."""

    terminal = ForeignKeyField(Terminal, db_column='terminal')

    @classmethod
    def _add(cls, group, terminal):
        """Adds a new member terminal."""
        member = cls()
        member.group = group
        member.terminal = terminal
        member.save()
        return member

    @classmethod
    def add(cls, group, terminal):
        """Adds a new member terminal iff it is not yet a member."""
        try:
            return cls.get((cls.group == group) & (cls.terminal == terminal))
        except DoesNotExist:
            return cls._add(group, terminal)


class MemberComcatAccount(Model, GroupMember):
    """Mapping between Comcat accounts and groups."""

    comcat_account = ForeignKeyField(ComcatAccount, db_column='terminal')

    @classmethod
    def _add(cls, group, comcat_account):
        """Adds a new member Comcat account."""
        member = cls()
        member.group = group
        member.comcat_account = comcat_account
        member.save()
        return member

    @classmethod
    def add(cls, group, comcat_account):
        """Adds a new member Comcat account iff it is not yet a member."""
        try:
            return cls.get(
                (cls.group == group) &
                (cls.comcat_account == comcat_account))
        except DoesNotExist:
            return cls._add(group, comcat_account)


class MemberTenement(Model, GroupMember):
    """Mapping between tenements and groups."""

    tenement = ForeignKeyField(Tenement, db_column='terminal')

    @classmethod
    def _add(cls, group, tenement):
        """Adds a new member tenement."""
        member = cls()
        member.group = group
        member.tenement = tenement
        member.save()
        return member

    @classmethod
    def add(cls, group, tenement):
        """Adds a new member tenement iff it is not yet a member."""
        try:
            return cls.get((cls.group == group) & (cls.tenement == tenement))
        except DoesNotExist:
            return cls._add(group, tenement)


class MemberProxy():
    """Proxy to tranparently handle a group's members."""

    def __init__(self, group):
        """Sets the respective group."""
        self.group = group

    def __iter__(self):
        """Yields all members of the respective group."""
        yield from MemberTerminal.select().where(
            MemberTerminal.group == self.group)
        yield from MemberComcatAccount.select().where(
            MemberComcatAccount.group == self.group)
        yield from MemberTenement.select().where(
            MemberTenement.group == self.group)

    def add(self, member):
        """Adds a member to the respective group."""
        if isinstance(member, Terminal):
            return MemberTerminal.add(self.group, member)
        elif isinstance(member, ComcatAccount):
            return MemberComcatAccount.add(self.group, member)
        elif isinstance(member, Tenement):
            return MemberTenement.add(self.group, member)
        else:
            raise UnsupportedMember(member) from None

    def remove(self, member):
        """Removes the respective member from the group."""
        if isinstance(member, Terminal):
            for member_terminal in MemberTerminal.select.where(
                    (MemberTerminal.group == self.group) &
                    (MemberTerminal.terminal == member)):
                member_terminal.delete_instance()
        elif isinstance(member, ComcatAccount):
            for member_comcat_account in MemberComcatAccount.select.where(
                    (MemberComcatAccount.group == self.group) &
                    (MemberComcatAccount.comcat_account == member)):
                member_comcat_account.delete_instance()
        elif isinstance(member, Tenement):
            for member_tenement in MemberTenement.select.where(
                    (MemberTenement.group == self.group) &
                    (MemberTenement.tenement == member)):
                member_tenement.delete_instance()
