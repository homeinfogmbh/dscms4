"""Facebook charts and associated data."""

from peewee import ForeignKeyField, IntegerField, SmallIntegerField, \
    BooleanField, CharField

from dscms4 import dom
from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model


__all__ = ['Facebook', 'Account']


UNCHANGED = object()    # Sentinel object to identify an unchanged value.


class Facebook(Chart):
    """Facebook data chart."""

    class Meta:
        table_name = 'chart_facebook'

    font_size = SmallIntegerField(default=26)
    title_color = IntegerField(default=0x000000)
    ken_burns = BooleanField(default=False)
    JSON_KEYS = {
        'fontSize': font_size, 'titleColor': title_color,
        'kenBurns': ken_burns}

    @classmethod
    def from_json(cls, json, **kwargs):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        accounts = json.pop('accounts', ())
        records = super().from_json(json, **kwargs)

        for account in accounts:
            account = Account.from_json(records.chart, account)
            records.append(account)

    def patch_json(self, json, **kwargs):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        try:
            accounts = json.pop('accounts')
        except KeyError:
            accounts = UNCHANGED

        records = super().patch_json(json, **kwargs)

        if accounts is not UNCHANGED:
            for account in self.accounts:
                account.delete_instance()

            for account in accounts:
                account = Account.from_json(chart, account)

    def to_json(self, *args, **kwargs):
        """Returns a JSON-ish dictionary."""
        json = super().to_json(*args, **kwargs)
        json['accounts'] = [account.to_json() for account in self.accounts]
        return json

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

    chart = ForeignKeyField(
        Facebook, column_name='chart', backref='accounts', on_delete='CASCADE')
    facebook_id = CharField(255)
    recent_days = SmallIntegerField(default=14)
    max_posts = SmallIntegerField(default=10)
    name = CharField(255, null=True)
    JSON_KEYS = {
        'facebookId': facebook_id, 'recentDays': recent_days,
        'maxPosts': max_posts}

    @classmethod
    def from_json(cls, json, chart, **kwargs):
        """Creates a new facebook account for the provided
        facebook chart from the respective distionary.
        """
        account = super().from_json(json, **kwargs)
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
