"""Object Relational Mappings"""

from datetime import datetime
from peewee import ForeignKeyField, CharField, TextField, \
    DateTimeField, BooleanField, IntegerField, SmallIntegerField

from homeinfo.crm import Customer
from filedb import FileProperty

from .common import DSCMS4Model, Schedule


class BaseChart(DSCMS4Model):
    """Abstract information and message container"""

    customer = ForeignKeyField(Customer, db_column='customer')
    title = CharField(255, null=True, default=None)
    text = TextField(null=True, default=None)
    created = DateTimeField()
    begins = DateTimeField(null=True, default=None)
    expires = DateTimeField(null=True, default=None)

    @property
    def active(self):
        """Determines whether the chart is considered active"""
        now = datetime.now()
        match_begins = self.begins is None or self.begins <= now
        match_expires = self.expires is None or self.expires >= now
        return match_begins and match_expires

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = {'created': self.created.isoformat()}

        if self.title is not None:
            dictionary['title'] = self.title

        if self.text is not None:
            dictionary['text'] = self.text

        if self.begins is not None:
            dictionary['begins'] = self.begins.isoformat()

        if self.expires is not None:
            dictionary['expires'] = self.expires.isoformat()

        return dictionary


class _Chart(DSCMS4Model):
    """Abstract chart class for extension"""

    base_chart = ForeignKeyField(BaseChart, db_column='base_chart')


class NewsChart(_Chart):
    """Chart to display news"""

    class Meta:
        db_table = 'news_chart'

    localization = CharField(255, null=True, default=None)

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = self.base_chart.to_dict()

        if self.localization is not None:
            dictionary['localization'] = self.localization

        return dictionary


class WeatherChart(_Chart):
    """Weather data"""

    class Meta:
        db_table = 'weather_chart'

    region = CharField(255)

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = self.base_chart.to_dict()

        if self.region is not None:
            dictionary['region'] = self.region

        return dictionary


class QuotesChart(_Chart):
    """Chart for quotations"""

    class Meta:
        db_table = 'quotes_chart'

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        return self.base_chart.to_dict()


class GuessPicture(_Chart):
    """Chart for guessing pictures"""

    class Meta:
        db_table = 'quotes_chart'


class FacebookChart(_Chart):
    """Facebook data chart"""

    class Meta:
        db_table = 'facebook_chart'

    days = SmallIntegerField(default=14)
    limit = SmallIntegerField(default=10)
    facebook_id = CharField(255)
    facebook_name = CharField(255)


class HTMLChart(_Chart):
    """A chart that may contain images"""

    class Meta:
        db_table = 'html_chart'

    random = BooleanField(default=False)
    loop_limit = SmallIntegerField()
    scale = BooleanField(default=False)
    fullscreen = BooleanField(default=False)
    ken_burns = BooleanField(default=False)


class VideoChart(_Chart):
    """A chart that may contain images and texts"""

    class Meta:
        db_table = 'video_chart'

    file = IntegerField()
    video = FileProperty(file)
    schedule = ForeignKeyField(Schedule, db_column='schedule')
