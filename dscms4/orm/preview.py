"""Preview tokens."""

from uuid import uuid4

from peewee import ForeignKeyField, UUIDField

from his import CUSTOMER
from terminallib import Terminal

from dscms4.messages.preview import NoSuchObject
from dscms4.orm.common import DSCMS4Model


__all__ = ['TYPES', 'TerminalPreviewToken']


class _PreviewToken(DSCMS4Model):
    """Common abstract preview token."""

    token = UUIDField(default=uuid4)
    obj = None

    @classmethod
    def generate(cls, ident):
        """Returns a token for the respective resource."""
        model = cls.obj.rel_model

        try:
            record = model.get(
                (model.id == ident) & (model.customer == CUSTOMER.id))
        except model.DoesNotExist:
            raise NoSuchObject(type=model.__name__)

        try:
            return cls.get(cls.obj == record)
        except cls.DoesNotExist:
            token = cls()
            token.obj = record
            token.save()
            return token


class TerminalPreviewToken(_PreviewToken):
    """Preview tokens for terminals."""

    class Meta:
        table_name = 'terminal_preview_token'

    obj = ForeignKeyField(
        Terminal, column_name='terminal', on_delete='CASCADE')


MODELS = (TerminalPreviewToken,)
TYPES = {'terminal': TerminalPreviewToken}
