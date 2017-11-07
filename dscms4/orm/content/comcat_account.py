"""ComCat account contents."""

from peewee import DoesNotExist, Model, ForeignKeyField

from comcat import Account

from ..charts import BaseChart
from ..common import DSCMS4Model
from ..configuration import Configuration
from ..menu import Menu
from ..ticker import Ticker

__all__ = [
    'ComCatAccountBaseChart',
    'ComCatAccountConfiguration',
    'ComCatAccountMenu',
    'ComCatAccountTicker']


class ComCatAccountContent(DSCMS4Model):
    """Common abstract content mapping."""

    comcat_account = ForeignKeyField(Account, db_column='comcat_account')
    content = None

    @classmethod
    def _add(cls, comcat_account, content):
        """Adds a new association of content with a ComCat account."""
        mapping = cls()
        mapping.comcat_account = comcat_account
        mapping.content = content
        return mapping

    @classmethod
    def add(cls, comcat_account, content):
        """Adds a new association of content with
        a ComCat account iff it does not yet exist.
        """
        try:
            return cls.get(
                (cls.comcat_account == comcat_account)
                & (cls.content == content))
        except DoesNotExist:
            return cls._add(comcat_account, content)


class ComCatAccountBaseChart(Model, ComCatAccountContent):
    """Association of a base chart with a ComCat account."""

    class Meta:
        db_table = 'comcat_account_base_chart'

    content = ForeignKeyField(BaseChart, db_column='base_chart')


class ComCatAccountConfiguration(Model, ComCatAccountContent):
    """Association of a configuration with a ComCat account."""

    class Meta:
        db_table = 'comcat_account_configuration'

    content = ForeignKeyField(Configuration, db_column='configuration')


class ComCatAccountMenu(Model, ComCatAccountContent):
    """Association of a menu with a ComCat account."""

    class Meta:
        db_table = 'comcat_account_menu'

    content = ForeignKeyField(Menu, db_column='menu')


class ComCatAccountTicker(Model, ComCatAccountContent):
    """Association of a ticker with a ComCat account."""

    class Meta:
        db_table = 'comcat_account_ticker'

    content = ForeignKeyField(Ticker, db_column='ticker')
