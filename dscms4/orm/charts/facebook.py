"""Facebook charts and associated data."""

from peewee import ForeignKeyField, IntegerField, SmallIntegerField, \
    BooleanField, CharField

from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model

__all__ = ['Facebook', 'Account']


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
            yield Account.from_dict(chart, account)

    def patch(self, dictionary, **kwargs):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        try:
            accounts = dictionary.pop('accounts')
        except KeyError:
            accounts = None

        base, chart = super().patch(dictionary, **kwargs)
        yield base
        yield chart

        if accounts is not None:
            for account in self.accounts:
                account.delete_instance()

            for account in accounts:
                yield Account.from_dict(chart, account)

    def to_dict(self, *args, **kwargs):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_dict(*args, **kwargs)
        dictionary['accounts'] = [
            account.to_dict() for account in self.accounts]
        return dictionary


class Account(DSCMS4Model):
    """Facebook account settings."""

    class Meta:
        table_name = 'facebook_account'

    chart = ForeignKeyField(
        Facebook, column_name='chart', backref='accounts', on_delete='CASCADE')
    facebook_id = CharField(255)
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
