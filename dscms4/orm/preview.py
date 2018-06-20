"""Preview tokens."""

from peewee import ForeignKeyField

from peeweeplus import UUID4Field
from terminallib import Terminal

from dscms4.orm.common import CustomerModel

__all__ = ['TerminalPreviewToken']


class _PreviewToken(CustomerModel):
    """Common abstract preview token."""

    token = UUID4Field()

    @classmethod
    def _obj_expression(cls, _):
        """Returns the respective object matching expression."""
        raise NotImplementedError()

    @classmethod
    def fetch(cls, token, customer, obj):
        """Fetches the token of the respective
        customer for the respective object.
        """
        return cls.get(
            (cls.token == token) & (cls.customer == customer)
            & cls._obj_expression(obj))


class TerminalPreviewToken(_PreviewToken):
    """Preview tokens for terminals."""

    class Meta:
        table_name = 'terminal_preview_token'

    terminal = ForeignKeyField(
        Terminal, column_name='terminal', on_delete='CASCADE')

    @classmethod
    def _obj_expression(cls, terminal):
        """Returns the terminal match."""
        return cls.terminal == terminal
