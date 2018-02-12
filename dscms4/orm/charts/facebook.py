"""Facebook charts and associated data."""

from fancylog import logging
from peewee import ForeignKeyField, IntegerField, SmallIntegerField, \
    BooleanField, CharField

from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model

__all__ = ['Facebook', 'Account']


@logging()
class Facebook(Chart):
    """Facebook data chart."""

    class Meta:
        table_name = 'chart_facebook'

    font_size = SmallIntegerField(default=26)
    title_color = IntegerField(default=0x000000)
    ken_burns = BooleanField(default=False)

    @classmethod
    def from_dict(cls, customer, dictionary, **kwargs):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        accounts = dictionary.pop('accounts', ())
        base, chart = super().from_dict(customer, dictionary, **kwargs)
        yield base
        yield chart

        for account in accounts:
            try:
                yield Account.from_dict(chart, account)
            except KeyError:
                cls.logger.error(
                    'Could not create account:', str(account), sep='\n')

    @property
    def accounts(self):
        """Yields accounts configured for this chart."""
        return Account.select().where(Account.facebook_chart == self)

    def to_dict(self):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_dict()
        dictionary['accounts'] = tuple(self.accounts)
        return dictionary


class Account(DSCMS4Model):
    """Facebook account settings."""

    class Meta:
        table_name = 'facebook_account'

    chart = ForeignKeyField(Facebook, column_name='chart', on_delete='CASCADE')
    facebook_id = IntegerField()
    recent_days = SmallIntegerField(default=14)
    max_posts = SmallIntegerField(default=10)
    name = CharField(255, null=True)

    @classmethod
    def from_dict(cls, chart, dictionary, **kwargs):
        """Creates a new facebook account for the provided
        facebook chart from the respective distionary.
        """
        account = super().from_dict(dictionary, **kwargs)
        account.chart = chart
        return account
