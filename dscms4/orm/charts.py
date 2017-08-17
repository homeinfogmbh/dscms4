"""Object Relational Mappings"""

from datetime import datetime

from peewee import ForeignKeyField, CharField, TextField, \
    DateTimeField, BooleanField, IntegerField, SmallIntegerField

from filedb import FileProperty

from .common import DSCMS4Model, CustomerModel, Schedule


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


class BaseChart(CustomerModel):
    """Abstract information and message container"""

    class Meta:
        db_table = 'chart'

    DEFAULT_DURATION = 10

    name = CharField(255, null=True, default=None)
    title = CharField(255, null=True, default=None)
    text = TextField(null=True, default=None)
    duration = SmallIntegerField(default=DEFAULT_DURATION)
    created = DateTimeField()
    schedule = ForeignKeyField(
        Schedule, db_column='schedule', null=True, default=None)

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a base chart from a dictionary
        for the respective customer
        """
        base_chart = cls()
        base_chart.customer = customer
        base_chart.name = dictionary.get('name')
        base_chart.title = dictionary.get('title')
        base_chart.text = dictionary.get('text')
        base_chart.duration = dictionary.get('duration', cls.DEFAULT_DURATION)
        base_chart.created = datetime.now()

        try:
            schedule = dictionary['schedule']
        except KeyError:
            pass
        else:
            base_chart.schedule = Schedule.from_dict(schedule)

        base_chart.save()
        return base_chart

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

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates the chart from the respective dictionary"""
        chart = cls()
        chart.chart = BaseChart.from_dict(customer, dictionary)
        # Do not invoke save() since this is an abstract class
        return chart

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

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a new local public transport chart
        from the dictionary for the respective customer
        """
        local_public_transport_chart = super().from_dict(customer, dictionary)
        local_public_transport_chart.save()
        return local_public_transport_chart


class NewsChart(Chart):
    """Chart to display news"""

    class Meta:
        db_table = 'news_chart'

    localization = CharField(255, null=True, default=None)

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a new news chart from the
        dictionary for the respective customer
        """
        news_chart = super().from_dict(customer, dictionary)
        news_chart.localization = dictionary.get('localization')
        news_chart.save()
        return news_chart

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

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer
        """
        quotes_chart = super().from_dict(customer, dictionary)
        quotes_chart.save()
        return quotes_chart


class VideoChart(Chart):
    """A chart that may contain images and texts"""

    class Meta:
        db_table = 'video_chart'

    file = IntegerField()
    video = FileProperty(file, file_client='foo')

    @classmethod
    def from_dict(cls, customer, dictionary, video):
        """Creates a new quotes chart from the
        dictionary for the respective customer
        """
        video_chart = super().from_dict(customer, dictionary)
        video_chart.video = video
        video_chart.save()
        return video_chart

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
