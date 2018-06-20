"""Preview tokens."""

from peewee import ForeignKeyField

from peeweeplus import UUID4Field
from terminallib import Terminal

from dscms4.orm.common import DSCMS4Model

__all__ = ['TerminalPreviewToken']


class _PreviewToken(DSCMS4Model):
    """Common abstract preview token."""

    token = UUID4Field()

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

    @property
    def obj(self):
        """Returns the terminal."""
        return self.terminal
