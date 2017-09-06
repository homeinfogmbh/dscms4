"""Object Relational Mappings"""

from datetime import datetime
from sys import stderr

from peewee import Model, ForeignKeyField, CharField, TextField, \
    DateTimeField, BooleanField, IntegerField, SmallIntegerField

from filedb import FileProperty

from .common import DSCMS4Model, CustomerModel
from .schedule import Schedule
# from .exceptions import InvalidData, MissingData


__all__ = ['Chart']


class NoTypeSpecified(Exception):
    """Indicates that no chart typ has been specified."""

    pass


class UnsupportedType(Exception):
    """Indicates that the specified chart type is not supported."""

    pass


def create_tables(fail_silently=True):
    """Create the respective tables."""

    for model in MODELS:
        try:
            model.create_table(fail_silently=fail_silently)
        except Exception:
            print('Could not create table for model "{}".'.format(model),
                  file=stderr)


class LocalPublicTtransportChart(Model, DSCMS4Model):
    """Local public transport chart."""

    class Meta:
        db_table = 'chart_local_public_transport'

    @classmethod
    def from_dict(cls, _):
        """Creates a new local public transport chart
        from the provided JSON compliant dictionary.
        """
        chart = cls()
        chart.save()
        return chart


class NewsChart(Model, DSCMS4Model):
    """Chart to display news."""

    class Meta:
        db_table = 'chart_news'

    localization = CharField(255, null=True, default=None)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new news chart from the
        provided JSON compliant dictionary.
        """
        chart = cls()
        chart.localization = dictionary.get('localization')
        chart.save()
        return chart

    def to_dict(self):
        """Converts the chart record into a JSON compliant dictionary."""
        dictionary = super().to_dict()

        if self.localization is not None:
            dictionary['localization'] = self.localization

        return dictionary


class QuotesChart(Model, DSCMS4Model):
    """Chart for quotations."""

    class Meta:
        db_table = 'chart_quotes'

    @classmethod
    def from_dict(cls, _):
        """Creates a new quotes chart."""
        chart = cls()
        chart.save()
        return chart


class VideoChart(Model, DSCMS4Model):
    """A chart that may contain images and texts"""

    class Meta:
        db_table = 'chart_video'

    file = IntegerField()
    video = FileProperty(file, file_client='foo')

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer
        """
        chart = cls()
        chart.video = dictionary['file']
        chart.save()
        return chart

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = super().to_dict()
        dictionary['file'] = self.file
        return dictionary


class HTMLChart(Model, DSCMS4Model):
    """A chart that may contain images"""

    class Meta:
        db_table = 'chart_html'

    random = BooleanField(default=False)
    loop_limit = SmallIntegerField(null=True, default=None)
    scale = BooleanField(default=False)
    fullscreen = BooleanField(default=False)
    ken_burns = BooleanField(default=False)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer
        """
        chart = cls()
        chart.random = dictionary.get('random')
        chart.loop_limit = dictionary.get('loop_limit')
        chart.scale = dictionary.get('scale')
        chart.fullscreen = dictionary.get('fullscreen')
        chart.ken_burns = dictionary.get('ken_burns')
        chart.save()
        return chart

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        return {
            'random': self.random,
            'loop_limit': self.loop_limit,
            'scale': self.scale,
            'fullscreen': self.fullscreen,
            'ken_burns': self.ken_burns}


class FacebookChart(Model, DSCMS4Model):
    """Facebook data chart"""

    class Meta:
        db_table = 'chart_facebook'

    days = SmallIntegerField(default=14)
    limit = SmallIntegerField(default=10)
    facebook_id = CharField(255)
    facebook_name = CharField(255)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer
        """
        chart = cls()
        chart.days = dictionary.get('days')
        chart.limit = dictionary.get('limit')
        chart.facebook_id = dictionary.get('facebook_id')
        chart.facebook_name = dictionary.get('facebook_name')
        chart.save()
        return chart

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        return {
            'days': self.days,
            'limit': self.limit,
            'facebook_id': self.facebook_id,
            'facebook_name': self.facebook_name}


class GuessPictureChart(Model, DSCMS4Model):
    """Chart for guessing pictures"""

    class Meta:
        db_table = 'chart_guess_picture'

    @classmethod
    def from_dict(cls, _):
        """Creates a new quotes chart from the
        dictionary for the respective customer
        """
        chart = cls()
        chart.save()
        return chart


class WeatherChart(Model, DSCMS4Model):
    """Weather data"""

    class Meta:
        db_table = 'chart_weather'

    @classmethod
    def from_dict(cls, _):
        """Creates a new quotes chart from the
        dictionary for the respective customer
        """
        chart = cls()
        chart.save()
        return chart


class TypeMap(Model, DSCMS4Model):
    """Mappings between base chart and chart implementations."""

    local_public_transport = ForeignKeyField(
        LocalPublicTtransportChart, db_column='local_public_transport_chart')
    news = ForeignKeyField(NewsChart, db_column='facebook_chart')
    quotes = ForeignKeyField(QuotesChart, db_column='quotes_chart')
    video = ForeignKeyField(VideoChart, db_column='video_chart')
    html = ForeignKeyField(HTMLChart, db_column='html_chart')
    facebook = ForeignKeyField(FacebookChart, db_column='facebook_chart')
    guess_picture = ForeignKeyField(
        GuessPictureChart, db_column='guess_picture_chart')
    weather = ForeignKeyField(WeatherChart, db_column='weather_chart')

    @classmethod
    def add(cls, typ):
        """Adds a type mapping to the respective type."""
        type_map = cls()

        if isinstance(typ, LocalPublicTtransportChart):
            type_map.local_public_transport = typ
        elif isinstance(typ, NewsChart):
            type_map.news = typ
        elif isinstance(typ, QuotesChart):
            type_map.quotes = typ
        elif isinstance(typ, VideoChart):
            type_map.video = typ
        elif isinstance(typ, HTMLChart):
            type_map.html = typ
        elif isinstance(typ, FacebookChart):
            type_map.facebook = typ
        elif isinstance(typ, GuessPictureChart):
            type_map.guess_picture = typ
        elif isinstance(typ, WeatherChart):
            type_map.weather = typ
        else:
            raise UnsupportedType(typ) from None

        type_map.save()
        return type_map

    @classmethod
    def from_dict(cls, dictionary):
        """Creates the type mapping from the respective dictionary."""
        try:
            class_name = dictionary['type']
        except KeyError:
            raise NoTypeSpecified() from None
        else:
            try:
                chart_class = TYPES[class_name]
            except KeyError:
                raise UnsupportedType(class_name) from None
            else:
                return cls.add(chart_class.from_dict(dictionary))

    @property
    def mappings(self):
        """Yields the mapped charts."""
        yield self.local_public_transport
        yield self.news
        yield self.quotes
        yield self.video
        yield self.html
        yield self.facebook
        yield self.guess_picture
        yield self.weather

    @property
    def chart(self):
        """Returns the mapped chart."""
        for chart in self.mappings:
            if chart is not None:
                return chart


class Chart(Model, CustomerModel):
    """Common chart model."""

    class Meta:
        db_table = 'chart'

    DEFAULT_DURATION = 10

    typ = ForeignKeyField(TypeMap, db_column='type')
    name = CharField(255, null=True, default=None)
    title = CharField(255, null=True, default=None)
    text = TextField(null=True, default=None)
    duration = SmallIntegerField(default=DEFAULT_DURATION)
    created = DateTimeField()
    schedule = ForeignKeyField(
        Schedule, db_column='schedule', null=True, default=None)

    @classmethod
    def add(cls, customer, typ, name=None, title=None, text=None,
            duration=None, schedule=None):
        """Adds a new chart."""
        chart = cls()
        chart.created = datetime.now()
        chart.customer = customer
        chart.typ = typ
        chart.name = name
        chart.title = title
        chart.text = text
        chart.duration = duration
        chart.schedule = schedule
        chart.save()
        return chart

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a base chart from a dictionary
        for the respective customer.
        """
        type_map = TypeMap.from_dict(dictionary)
        schedule = dictionary.get('schedule')

        if schedule:
            schedule = Schedule.from_dict(schedule)
        else:
            schedule = None

        return cls.add(
            customer,
            type_map,
            name=dictionary.get('name'),
            title=dictionary.get('title'),
            text=dictionary.get('text'),
            duration=dictionary.get('duration'),
            schedule=schedule)

    @property
    def active(self):
        """Determines whether the chart is considered active"""
        return self.schedule is None or self.schedule.active

    @property
    def implementation(self):
        """Returns the mapped implementation of this chart."""
        return self.typ.chart

    def _to_dict(self):
        """Returns a JSON compatible dictionary"""
        return {
            'id': self.id,
            'created': self.created.isoformat(),
            'name': self.name,
            'title': self.title,
            'text': self.text,
            'duration': self.duration,
            'schedule': self.schedule.id}

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = self._to_dict()

        try:
            implementation_dict_method = self.implementation.to_dict
        except AttributeError:
            pass
        else:
            dictionary.update(implementation_dict_method())

        return dictionary


CHARTS = [
    LocalPublicTtransportChart, NewsChart, QuotesChart, VideoChart, HTMLChart,
    FacebookChart, GuessPictureChart, WeatherChart]
TYPES = {chart.__class__.__name__: chart for chart in CHARTS}
MODELS = CHARTS + [TypeMap, Chart]
