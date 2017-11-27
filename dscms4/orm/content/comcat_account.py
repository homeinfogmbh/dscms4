"""Content assigned to ComCat accounts."""

from peewee import DoesNotExist, Model, ForeignKeyField

from comcat import Account

from dscms4.orm.charts import BaseChart
from dscms4.orm.common import DSCMS4Model
from dscms4.orm.configuration import Configuration
from dscms4.orm.menu import Menu
from dscms4.orm.ticker import Ticker

__all__ = [
    'ComCatAccountBaseChart',
    'ComCatAccountConfiguration',
    'ComCatAccountMenu',
    'ComCatAccountTicker']


class ComCatAccountContent(DSCMS4Model):
    """Common abstract content mapping."""

    comcat_account = ForeignKeyField(Account, db_column='comcat_account')


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
