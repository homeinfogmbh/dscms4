"""Object Relational Mappings"""

from datetime import datetime

from peewee import Model, ForeignKeyField, CharField, TextField, \
    DateTimeField, BooleanField, IntegerField, SmallIntegerField

from filedb import FileProperty

from .common import CustomerModel, Schedule
# from .exceptions import InvalidData, MissingData


__all__ = [
    'LocalPublicTtransportChart',
    'NewsChart',
    'QuotesChart',
    'VideoChart',
    'HTMLChart',
    'FacebookChart',
    'GuessPictureChart',
    'WeatherChart',
    'MODELS',
    'CHARTS']


class Chart(CustomerModel):
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
        chart = cls()
        chart.customer = customer
        chart.name = dictionary.get('name')
        chart.title = dictionary.get('title')
        chart.text = dictionary.get('text')
        chart.duration = dictionary.get('duration', cls.DEFAULT_DURATION)
        chart.created = datetime.now()
        chart.schedule = dictionary.get('schedule')
        # Do not ivoke save() here since implemented model may be incomplete
        return chart

    @property
    def active(self):
        """Determines whether the chart is considered active"""
        return self.schedule is None or self.schedule.active

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = {
            'type': self.__class__.__name__,
            'id': self.id,
            'created': self.created.isoformat()}

        if self.name is not None:
            dictionary['name'] = self.name

        if self.title is not None:
            dictionary['title'] = self.title

        if self.text is not None:
            dictionary['text'] = self.text

        if self.duration is not None:
            dictionary['duration'] = self.duration

        if self.schedule is not None:
            dictionary['schedule'] = self.schedule.id

        return dictionary


class LocalPublicTtransportChart(Model, Chart):
    """Local public transport chart"""

    class Meta:
        db_table = 'chart_local_public_transport'

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a new local public transport chart
        from the dictionary for the respective customer
        """
        local_public_transport_chart = super().from_dict(customer, dictionary)
        local_public_transport_chart.save()
        return local_public_transport_chart


class NewsChart(Model, Chart):
    """Chart to display news"""

    class Meta:
        db_table = 'chart_news'

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


class QuotesChart(Model, Chart):
    """Chart for quotations"""

    class Meta:
        db_table = 'chart_quotes'

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer
        """
        quotes_chart = super().from_dict(customer, dictionary)
        quotes_chart.save()
        return quotes_chart


class VideoChart(Model, Chart):
    """A chart that may contain images and texts"""

    class Meta:
        db_table = 'chart_video'

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

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = super().to_dict()
        dictionary['file'] = self.file
        return dictionary


class HTMLChart(Model, Chart):
    """A chart that may contain images"""

    class Meta:
        db_table = 'chart_html'

    random = BooleanField(default=False)
    loop_limit = SmallIntegerField(null=True, default=None)
    scale = BooleanField(default=False)
    fullscreen = BooleanField(default=False)
    ken_burns = BooleanField(default=False)

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer
        """
        html_chart = super().from_dict(customer, dictionary)
        html_chart.random = dictionary.get('random')
        html_chart.loop_limit = dictionary.get('loop_limit')
        html_chart.scale = dictionary.get('scale')
        html_chart.fullscreen = dictionary.get('fullscreen')
        html_chart.ken_burns = dictionary.get('ken_burns')
        html_chart.save()
        return html_chart

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = super().to_dict()
        dictionary['random'] = self.random
        dictionary['loop_limit'] = self.loop_limit
        dictionary['scale'] = self.scale
        dictionary['fullscreen'] = self.fullscreen
        dictionary['ken_burns'] = self.ken_burns
        return dictionary


class FacebookChart(Model, Chart):
    """Facebook data chart"""

    class Meta:
        db_table = 'chart_facebook'

    days = SmallIntegerField(default=14)
    limit = SmallIntegerField(default=10)
    facebook_id = CharField(255)
    facebook_name = CharField(255)

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer
        """
        facebook_chart = super().from_dict(customer, dictionary)
        facebook_chart.days = dictionary.get('days')
        facebook_chart.limit = dictionary.get('limit')
        facebook_chart.facebook_id = dictionary.get('facebook_id')
        facebook_chart.facebook_name = dictionary.get('facebook_name')
        facebook_chart.save()
        return facebook_chart

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
        db_table = 'chart_guess_picture'

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer
        """
        guess_picture_chart = super().from_dict(customer, dictionary)
        guess_picture_chart.save()
        return guess_picture_chart


class WeatherChart(Chart):
    """Weather data"""

    class Meta:
        db_table = 'chart_weather'

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer
        """
        weather_chart = super().from_dict(customer, dictionary)
        weather_chart.save()
        return weather_chart


MODELS = [
    LocalPublicTtransportChart, NewsChart, QuotesChart, VideoChart, HTMLChart,
    FacebookChart, GuessPictureChart, WeatherChart]
CHARTS = {chart.__class__.__name__: chart for chart in MODELS}
