"""Preview tokens."""

from peewee import ForeignKeyField

from peeweeplus import UUID4Field
from terminallib import Terminal

from dscms4.messages.terminal import NoSuchTerminal
from dscms4.orm.common import DSCMS4Model

__all__ = ['TYPES', 'TerminalPreviewToken']


class _PreviewToken(DSCMS4Model):
    """Common abstract preview token."""

    token = UUID4Field()

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

    terminal = ForeignKeyField(
        Terminal, column_name='terminal', on_delete='CASCADE')

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
