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
    schedule = ForeignKeyField(
        Schedule, db_column='schedule', null=True, default=None)

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

        if self.schedule is not None:
            dictionary['schedule'] = self.schedule.to_dict()

        return dictionary


class _Chart(DSCMS4Model):
    """Abstract chart class for extension"""

    base_chart = ForeignKeyField(BaseChart, db_column='base_chart')

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        return self.base_chart.to_dict()


class LPT(_Chart):
    """Local public transport chart"""

    class Meta:
        db_table = 'lpt_chart'


class NewsChart(_Chart):
    """Chart to display news"""

    class Meta:
        db_table = 'news_chart'

    localization = CharField(255, null=True, default=None)

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = super().to_dict()

        if self.localization is not None:
            dictionary['localization'] = self.localization

        return dictionary


class QuotesChart(_Chart):
    """Chart for quotations"""

    class Meta:
        db_table = 'quotes_chart'

class VideoChart(_Chart):
    """A chart that may contain images and texts"""

    class Meta:
        db_table = 'video_chart'

    file = IntegerField()
    video = FileProperty(file)

    def to_dict(self, file_name=None):
        """Returns a JSON compatible dictionary"""
        dictionary = super().to_dict()
        dictionary['file'] = self.file
        return dictionary


class HTMLChart(_Chart):
    """A chart that may contain images"""

    class Meta:
        db_table = 'html_chart'

    random = BooleanField(default=False)
    loop_limit = SmallIntegerField()
    scale = BooleanField(default=False)
    fullscreen = BooleanField(default=False)
    ken_burns = BooleanField(default=False)

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = super().to_dict()
        dictionary['random'] = self.random
        dictionary['loop_limit'] = self.loop_limit
        dictionary['scale'] = self.scale
        dictionary['fullscreen'] = self.fullscreen
        dictionary['ken_burns'] = self.ken_burns
        return dictionary


class FacebookChart(_Chart):
    """Facebook data chart"""

    class Meta:
        db_table = 'facebook_chart'

    days = SmallIntegerField(default=14)
    limit = SmallIntegerField(default=10)
    facebook_id = CharField(255)
    facebook_name = CharField(255)

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = super().to_dict()
        dictionary['days'] = self.days
        dictionary['limit'] = self.limit
        dictionary['facebook_id'] = self.facebook_id
        dictionary['facebook_name'] = self.facebook_name
        return dictionary


class GuessPicture(_Chart):
    """Chart for guessing pictures"""

    class Meta:
        db_table = 'quotes_chart'


class Text(_Chart):
    """Simple text chart"""

    class Meta:
        db_table = 'text_chart'

    text = TextField()

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = super().to_dict()
        dictionary['text'] = self.text
        return dictionary


class WeatherChart(_Chart):
    """Weather data"""

    class Meta:
        db_table = 'weather_chart'
