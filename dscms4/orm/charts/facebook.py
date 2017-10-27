"""Facebook charts and associated data."""

from fancylog import logging
from peewee import Model, ForeignKeyField, IntegerField, SmallIntegerField, \
    BooleanField, CharField

from dscms4.orm.common import DSCMS4Model
from dscms4.orm.charts.common import Chart

__all__ = ['Facebook', 'Account']


DEFAULT_FONT_SIZE = 26
DEFAULT_TITLE_COLOR = 0x000000
DEFAULT_KEN_BURNS = False
DEFAULT_RECENT_DAYS = 14
DEFAULT_MAX_POSTS = 10


@logging()
class Facebook(Model, Chart):
    """Facebook data chart."""

    class Meta:
        db_table = 'chart_facebook'

    font_size = SmallIntegerField(default=DEFAULT_FONT_SIZE)
    title_color = IntegerField(default=DEFAULT_TITLE_COLOR)
    ken_burns = BooleanField(default=DEFAULT_KEN_BURNS)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        chart = super().from_dict(dictionary)
        chart.font_size = dictionary.get('font_size', DEFAULT_FONT_SIZE)
        chart.title_color = dictionary.get('title_color', DEFAULT_TITLE_COLOR)
        chart.ken_burns = dictionary.get('ken_burns', DEFAULT_KEN_BURNS)
        yield chart

        for account in dictionary.get('accounts', ()):
            try:
                yield Account.from_dict(chart, account)
            except KeyError:
                cls.logger.error(
                    'Could not create account:', str(account), sep='\n')

    @property
    def accounts(self):
        """Yields accounts configured for this chart."""
        return Account.select().where(Account.facebook_chart == self)

    @property
    def dictionary(self):
        """Returns a JSON-ish dictionary of the record's fields."""
        return {
            'font_size': self.font_size,
            'title_color': self.title_color,
            'ken_burns': self.ken_burns,
            'accounts': tuple(self.accounts)}

    def to_dict(self):
        """Returns a JSON-ish dictionary."""
        dictionary = super.to_dict()
        dictionary.update(self.dictionary)
        return dictionary


class Account(Model, DSCMS4Model):
    """Facebook account settings."""

    class Meta:
        db_table = 'facebook_account'

    facebook_chart = ForeignKeyField(FacebookChart, db_column='facebook_chart')
    facebook_id = IntegerField()
    recent_days = SmallIntegerField(default=DEFAULT_RECENT_DAYS)
    max_posts = SmallIntegerField(default=DEFAULT_MAX_POSTS)
    name = CharField(255, null=True, default=None)

    @classmethod
    def from_dict(cls, facebook_chart, dictionary):
        """Creates a new facebook account for the provided
        facebook chart from the respective distionary.
        """
        account = cls()
        account.facebook_chart = facebook_chart
        account.facebook_id = dictionary['facebook_id']
        account.recent_days = dictionary.get(
            'recent_days', DEFAULT_RECENT_DAYS)
        account.max_posts = dictionary.get('max_posts', DEFAULT_MAX_POSTS)
        account.name = dictionary.get('name')
        return account

    @property
    def dictionary(self):
        """Returns a JSON-ish dictionary of the record's fields."""
        return {
            'facebook_chart': self.facebook_chart.id,
            'facebook_id': self.facebook_id,
            'recent_days': self.recent_days,
            'max_posts': self.max_posts,
            'name': self.name}

    def to_dict(self):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_dict()
        dictionary.update(self.dictionary)
        return dictionary
