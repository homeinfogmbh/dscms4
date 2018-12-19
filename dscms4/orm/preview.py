"""Preview tokens."""

from uuid import uuid4

from peewee import ForeignKeyField, UUIDField

from his import CUSTOMER
from terminallib import Terminal

from dscms4.messages.preview import NoSuchObject
from dscms4.orm.common import DSCMS4Model
from dscms4.orm.group import Group


__all__ = ['TYPES', 'TerminalPreviewToken', 'GroupPreviewToken']


class _PreviewToken(DSCMS4Model):
    """Common abstract preview token."""

    token = UUIDField(default=uuid4)
    obj = None

    @staticmethod
    def identify(model, ident):
        """Returns a selector to identify the respective model."""
        raise NotImplementedError()

    @classmethod
    def generate(cls, ident):
        """Returns a token for the respective resource."""
        model = cls.obj.rel_model

        try:
            record = model.get(
                cls.identify(model, ident) & (model.customer == CUSTOMER.id))
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

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'terminal_preview_token'

    obj = ForeignKeyField(
        Terminal, column_name='terminal', on_delete='CASCADE')

    @staticmethod
    def identify(model, ident):
        """Identifies the terminal by TID."""
        return model.tid == ident


class GroupPreviewToken(_PreviewToken):
    """Preview tokens for groups."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'group_preview_token'

    obj = ForeignKeyField(Group, column_name='group', on_delete='CASCADE')

    @staticmethod
    def identify(model, ident):
        """Identifies the group by its ID."""
        return model.id == ident


MODELS = (TerminalPreviewToken, GroupPreviewToken)
TYPES = {'terminal': TerminalPreviewToken, 'group': GroupPreviewToken}
