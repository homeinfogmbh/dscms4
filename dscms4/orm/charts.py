"""Object Relational Mappings"""

from peewee import ForeignKeyField, CharField, TextField, \
    DateTimeField, BooleanField, IntegerField, SmallIntegerField

from homeinfo.crm import Customer
from filedb import FileProperty

from .common import DSCMS4Model, Schedule


__all__ = [
    'BaseChart',
    'Chart',
    'LocalPublicTtransportChart',
    'NewsChart',
    'QuotesChart',
    'VideoChart',
    'HTMLChart',
    'FacebookChart',
    'GuessPictureChart',
    'WeatherChart']


class BaseChart(DSCMS4Model):
    """Abstract information and message container"""

    class Meta:
        db_table = 'chart'

    customer = ForeignKeyField(Customer, db_column='customer')
    name = CharField(255, null=True, default=None)
    title = CharField(255, null=True, default=None)
    text = TextField(null=True, default=None)
    duration = SmallIntegerField(default=10)
    created = DateTimeField()
    schedule = ForeignKeyField(
        Schedule, db_column='schedule', null=True, default=None)

    @property
    def active(self):
        """Determines whether the chart is considered active"""
        return self.schedule is None or self.schedule.active

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = {'created': self.created.isoformat()}

        if self.name is not None:
            dictionary['name'] = self.name

        if self.title is not None:
            dictionary['title'] = self.title

        if self.text is not None:
            dictionary['text'] = self.text

        if self.duration is not None:
            dictionary['duration'] = self.duration

        if self.schedule is not None:
            dictionary['schedule'] = self.schedule.to_dict()

        return dictionary


class Chart(DSCMS4Model):
    """Abstract chart class for extension"""

    chart = ForeignKeyField(BaseChart, db_column='chart')

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        return self.chart.to_dict()

    def delete_instance(self, delete_basechart=True, **kwargs):
        """Deletes the ORM instance from the database"""
        result = super().delete_instance(**kwargs)

        if delete_basechart:
            self.chart.delete_instance(**kwargs)

        return result


class LocalPublicTtransportChart(Chart):
    """Local public transport chart"""

    class Meta:
        db_table = 'local_public_transport_chart'

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        return {}


class NewsChart(Chart):
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


class QuotesChart(Chart):
    """Chart for quotations"""

    class Meta:
        db_table = 'quotes_chart'


class VideoChart(Chart):
    """A chart that may contain images and texts"""

    class Meta:
        db_table = 'video_chart'

    file = IntegerField()
    video = FileProperty(file, file_client='foo')

    def to_dict(self, file_name=None):
        """Returns a JSON compatible dictionary"""
        dictionary = super().to_dict()
        dictionary['file'] = self.file
        return dictionary


class HTMLChart(Chart):
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


class FacebookChart(Chart):
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


class GuessPictureChart(Chart):
    """Chart for guessing pictures"""

    class Meta:
        db_table = 'guess_picture_chart'


class WeatherChart(Chart):
    """Weather data"""

    class Meta:
        db_table = 'weather_chart'
