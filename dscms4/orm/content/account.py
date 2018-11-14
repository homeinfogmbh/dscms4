"""Content assigned to ComCat accounts."""

from peewee import ForeignKeyField, IntegerField

from comcat import Account

from dscms4.orm.charts import ChartMode, BaseChart
from dscms4.orm.common import DSCMS4Model
from dscms4.orm.configuration import Configuration
from dscms4.orm.menu import Menu


__all__ = [
    'AccountBaseChart',
    'AccountConfiguration',
    'AccountMenu',
    'MODELS']


class _AccountContent(DSCMS4Model):
    """Common abstract content mapping."""

    account = ForeignKeyField(
        Account, column_name='account', on_delete='CASCADE')


class AccountBaseChart(_AccountContent):
    """Association of a base chart with an account."""

    class Meta:
        table_name = 'account_base_chart'

    base_chart = ForeignKeyField(
        BaseChart, column_name='base_chart', on_delete='CASCADE')
    index = IntegerField(default=0)

    @classmethod
    def from_json(cls, json, account, base_chart, **kwargs):
        """Creates a new group base chart."""
        record = super().from_json(json, **kwargs)
        record.account = account
        record.base_chart = base_chart
        return record

    @property
    def chart(self):
        """Returns the respective chart."""
        return self.base_chart.chart

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {
            'id': self.id,
            'chart': self.chart.to_json(mode=ChartMode.BRIEF),
            'index': self.index}


class AccountConfiguration(_AccountContent):
    """Association of a configuration with an account."""

    class Meta:
        table_name = 'account_configuration'

    configuration = ForeignKeyField(
        Configuration, column_name='configuration', on_delete='CASCADE')

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {'id': self.id, 'configuration': self.configuration_id}


class AccountMenu(_AccountContent):
    """Association of a menu with an account."""

    class Meta:
        table_name = 'account_menu'

    menu = ForeignKeyField(Menu, column_name='menu', on_delete='CASCADE')

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {'id': self.id, 'menu': self.menu_id}


MODELS = (AccountBaseChart, AccountConfiguration, AccountMenu)
