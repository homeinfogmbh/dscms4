"""Facebook charts and associated data."""

from peewee import Model, ForeignKeyField, IntegerField, SmallIntegerField, \
    BooleanField, CharField

from dscms4.orm.common import DSCMS4Model
from dscms4.orm.charts.common import Chart


class FacebookChart(Model, Chart):
    """Facebook data chart."""

    class Meta:
        db_table = 'chart_facebook'

    font_size = SmallIntegerField(default=26)
    title_color = IntegerField(default=0x000000)
    ken_burns = BooleanField(default=False)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        chart = super().from_dict(dictionary)
        chart.font_size = dictionary.get('font_size', 26)
        chart.title_color = dictionary.get('title_color', 0x000000)
        chart.ken_burns = dictionary.get('ken_burns', False)
        chart.save()
        return chart

    @property
    def dictionary(self):
        """Returns a JSON compliant dictionary of this chart's fields."""
        return {
            'font_size': self.font_size,
            'title_color': self.title_color,
            'ken_burns': self.ken_burns}

    def to_dict(self):
        """Returns a JSON compatible dictionary."""
        dictionary = super.to_dict()
        dictionary.update(self.dictionary)
        return dictionary


class FacebookAccount(Model, DSCMS4Model):
    """Facebook account settings."""

    class Meta:
        db_table = 'facebook_account'

    facebook_chart = ForeignKeyField(FacebookChart, db_column='facebook_chart')
    facebook_id = IntegerField()
    recent_days = SmallIntegerField(default=14)
    max_posts = SmallIntegerField(default=10)
    name = CharField(255, null=True, default=None)

    @classmethod
    def from_dict(cls, facebook_chart, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        chart = super().from_dict(dictionary)
        chart.facebook_chart = facebook_chart
        chart.facebook_id = dictionary['facebook_id']
        chart.recent_days = dictionary.get('recent_days', 14)
        chart.max_posts = dictionary.get('max_posts', 10)
        chart.name = dictionary.get('name')
        chart.save()
        return chart

    @property
    def dictionary(self):
        """Returns a JSON-ish dictionary."""
        return {
            'facebook_chart': self.facebook_chart,
            'facebook_id': self.facebook_id,
            'recent_days': self.recent_days,
            'max_posts': self.max_posts,
            'name': self.name}

    def to_dict(self):
        """Returns a JSON compliant dictionary."""
        dictionary = super().to_dict()
        dictionary.update(self.dictionary)
        return dictionary
