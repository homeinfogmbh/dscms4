"""Preview tokens."""

from peewee import ForeignKeyField

from peeweeplus import UUID4Field
from terminallib import Terminal

from dscms4.orm.common import DSCMS4Model

__all__ = ['TYPES', 'TerminalPreviewToken']


class _PreviewToken(DSCMS4Model):
    """Common abstract preview token."""

    token = UUID4Field()

    @classmethod
    def generate(cls, ident):
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
    def generate(cls, ident):
        """Returns a token for the respective terminal."""
        try:
            return cls.get(cls.terminal == ident)
        except cls.DoesNotExist:
            token = cls()
            token.terminal = ident
            token.save()
            return token

    @property
    def obj(self):
        """Returns the terminal."""
        return self.terminal


TYPES = {
    'terminal': TerminalPreviewToken
}
