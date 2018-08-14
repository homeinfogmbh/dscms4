"""Preview tokens."""

from uuid import uuid4

from peewee import ForeignKeyField, UUIDField

from peeweeplus import JSONField
from terminallib import Terminal

from dscms4.messages.terminal import NoSuchTerminal
from dscms4.orm.common import DSCMS4Model

__all__ = ['TYPES', 'TerminalPreviewToken']


class _PreviewToken(DSCMS4Model):
    """Common abstract preview token."""

    token = JSONField(UUIDField, default=uuid4)

    @classmethod
    def generate(cls, ident, customer):
        """Returns a token for the respective resource."""
        raise NotImplementedError()

    @property
    def obj(self):
        """Returns the referenced object."""
        raise NotImplementedError()


class TerminalPreviewToken(_PreviewToken):
    """Preview tokens for terminals."""

    class Meta:
        table_name = 'terminal_preview_token'

    terminal = JSONField(
        ForeignKeyField, Terminal, column_name='terminal', on_delete='CASCADE')

    @classmethod
    def generate(cls, ident, customer):
        """Returns a token for the respective terminal."""
        try:
            terminal = Terminal.get(
                (Terminal.id == ident) & (Terminal.customer == customer))
        except Terminal.DoesNotExist:
            raise NoSuchTerminal()

        try:
            return cls.get(cls.terminal == terminal)
        except cls.DoesNotExist:
            token = cls()
            token.terminal = terminal
            token.save()
            return token

    @property
    def obj(self):
        """Returns the terminal."""
        return self.terminal


TYPES = {
    'terminal': TerminalPreviewToken
}
