"""Facebook charts and associated data."""

from fancylog import logging
from peewee import ForeignKeyField, IntegerField, SmallIntegerField, \
    BooleanField, CharField

from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model

__all__ = ['Facebook', 'Account']


DEFAULT_FONT_SIZE = 26
DEFAULT_TITLE_COLOR = 0x000000
DEFAULT_KEN_BURNS = False
DEFAULT_RECENT_DAYS = 14
DEFAULT_MAX_POSTS = 10


@logging()
class Facebook(DSCMS4Model, Chart):
    """Facebook data chart."""

    class Meta:
        db_table = 'chart_facebook'

    font_size = SmallIntegerField(default=DEFAULT_FONT_SIZE)
    title_color = IntegerField(default=DEFAULT_TITLE_COLOR)
    ken_burns = BooleanField(default=DEFAULT_KEN_BURNS)

    @classmethod
    def from_dict(cls, dictionary, customer=None):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        chart = super().from_dict(dictionary, customer=customer)
        yield chart

        for account in dictionary.get('accounts', tuple()):
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
        dictionary = super.to_dict()
        dictionary['accounts'] = tuple(self.accounts)
        return dictionary


class Account(DSCMS4Model):
    """Facebook account settings."""

    class Meta:
        db_table = 'facebook_account'

    chart = ForeignKeyField(Facebook, db_column='facebook_chart')
    facebook_id = IntegerField()
    recent_days = SmallIntegerField(default=DEFAULT_RECENT_DAYS)
    max_posts = SmallIntegerField(default=DEFAULT_MAX_POSTS)
    name = CharField(255, null=True, default=None)

    @classmethod
    def from_dict(cls, chart, dictionary):
        """Creates a new facebook account for the provided
        facebook chart from the respective distionary.
        """
        account = super().from_dict(dictionary)
        account.chart = chart
        return account
