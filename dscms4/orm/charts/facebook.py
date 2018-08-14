"""Facebook charts and associated data."""

from peewee import ForeignKeyField, IntegerField, SmallIntegerField, \
    BooleanField, CharField

from peeweeplus import JSONField

from dscms4 import dom
from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model

__all__ = ['Facebook', 'Account']


class Facebook(Chart):
    """Facebook data chart."""

    class Meta:
        table_name = 'chart_facebook'

    font_size = JSONField(SmallIntegerField, default=26, key='fontSize')
    title_color = JSONField(IntegerField, default=0x000000, key='titleColor')
    ken_burns = JSONField(BooleanField, default=False, key='kenBurns')

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

    def to_dom(self, brief=False):
        """Returns an XML DOM of this chart."""
        if brief:
            return super().to_dom(dom.BriefChart)

        xml = super().to_dom(dom.Facebook)
        xml.font_size = self.font_size
        xml.title_color = self.title_color
        xml.ken_burns = self.ken_burns
        xml.account = [account.to_dom() for account in self.accounts]
        return xml


class Account(DSCMS4Model):
    """Facebook account settings."""

    class Meta:
        table_name = 'facebook_account'

    chart = JSONField(
        ForeignKeyField, Facebook, column_name='chart', backref='accounts',
        on_delete='CASCADE')
    facebook_id = JSONField(CharField, 255, key='facebookId')
    recent_days = JSONField(SmallIntegerField, default=14, key='recentDays')
    max_posts = JSONField(SmallIntegerField, default=10, key='maxPosts')
    name = JSONField(CharField, 255, null=True)

    @classmethod
    def from_dict(cls, chart, dictionary, **kwargs):
        """Creates a new facebook account for the provided
        facebook chart from the respective distionary.
        """
        account = super().from_dict(dictionary, **kwargs)
        account.chart = chart
        return account

    def to_dom(self):
        """Returns an XML DOM of this model."""
        xml = dom.FacebookAccount()
        xml.facebook_id = self.facebook_id
        xml.recent_days = self.recent_days
        xml.max_posts = self.max_posts
        xml.name = self.name
        return xml
