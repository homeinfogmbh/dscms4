"""Object Relational Mappings"""

from datetime import datetime
from enum import Enum
from sys import stderr

from peewee import Model, ForeignKeyField, CharField, TextField, \
    DateTimeField, BooleanField, IntegerField, SmallIntegerField

from filedb import FileProperty, FileClient
from peeweeplus import EnumField

from .common import DSCMS4Model, CustomerModel
from .schedule import Schedule
# from .exceptions import InvalidData, MissingData


__all__ = ['Chart']

DEFAULT_DURATION = 10
FILE_CLIENT = FileClient('c33696ee-49bb-459d-a2c4-80574691de91')


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


class TransitionEffect(Enum):
    """Effects available for chart transitions."""

    FADE_IN = 'fade-in'
    MOSAIK = 'mosaik'
    SLIDE_IN = 'slide-in'
    RANDOM = 'random'
    NONE = None


class BaseChart(Model, CustomerModel):
    """Common basic chart data model."""

    class Meta:
        db_table = 'base_chart'

    title = CharField(255)
    description = TextField(null=True, default=None)
    duration = SmallIntegerField(default=DEFAULT_DURATION)
    created = DateTimeField()
    schedule = ForeignKeyField(
        Schedule, db_column='schedule', null=True, default=None)
    transition_effect = EnumField(TransitionEffect)

    @classmethod
    def add(cls, customer, title, description=None, duration=None,
            schedule=None, transition_effect=TransitionEffect.NONE):
        """Adds a new chart."""
        chart = cls()
        chart.customer = customer
        chart.title = title
        chart.description = description
        chart.duration = duration
        chart.created = datetime.now()
        chart.schedule = schedule
        chart.transition_effect = transition_effect
        chart.save()
        return chart

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a base chart from a dictionary
        for the respective customer.
        """
        try:
            schedule = Schedule.from_dict(dictionary['schedule'])
        except KeyError:
            schedule = None

        return cls.add(
            customer,
            dictionary['title'],
            description=dictionary.get('description'),
            duration=dictionary.get('duration'),
            schedule=schedule,
            transition_effect=dictionary.get('description'))

    @property
    def active(self):
        """Determines whether the chart is considered active."""
        return self.schedule is None or self.schedule.active

    @property
    def chart(self):
        """Returns the mapped implementation of this chart."""
        # TODO: implement
        pass

    def to_dict(self, cascade=False):
        """Returns a JSON compatible dictionary."""
        dictionary = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'duration': self.duration,
            'created': self.created.isoformat(),
            'transition_effect': self.transition_effect.value}

        if self.schedule:
            if cascade:
                dictionary['schedule'] = self.schedule.to_dict()
            else:
                dictionary['schedule'] = self.schedule.id

        return dictionary


class Chart(DSCMS4Model):
    """Abstract basic chart."""

    base_chart = ForeignKeyField(BaseChart, db_column='base_chart')

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new chart from the respective dictionary."""
        base_chart = BaseChart.from_dict(dictionary)
        chart = cls()
        chart.base_chart = base_chart
        return chart

    def to_dict(self):
        """Converts the chart into a JSON compliant dictionary."""
        return self.base_chart.to_dict()


class LocalPublicTtransportChart(Model, Chart):
    """Local public transport chart."""

    class Meta:
        db_table = 'chart_local_public_transport'


class NewsChart(Model, Chart):
    """Chart to display news."""

    class Meta:
        db_table = 'chart_news'

    localization = CharField(255, null=True, default=None)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new news chart from the
        provided JSON compliant dictionary.
        """
        chart = super().from_dict(dictionary)
        chart.localization = dictionary.get('localization')
        chart.save()
        return chart

    def to_dict(self):
        """Converts the chart record into a JSON compliant dictionary."""
        dictionary = super().to_dict()

        if self.localization is not None:
            dictionary['localization'] = self.localization

        return dictionary


class QuotesChart(Model, Chart):
    """Chart for quotations."""

    class Meta:
        db_table = 'chart_quotes'

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart."""
        chart = super().from_dict(dictionary)
        chart.save()
        return chart


class VideoChart(Model, Chart):
    """A chart that may contain images and texts."""

    class Meta:
        db_table = 'chart_video'

    file = IntegerField()
    video = FileProperty(file, file_client=FILE_CLIENT)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        chart = super().from_dict(dictionary)
        chart.video = dictionary['file']
        chart.save()
        return chart

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = super().to_dict()
        dictionary['file'] = self.file
        return dictionary


class ImageTextChart(Model, Chart):
    """A chart that may contain images and text."""

    class Meta:
        db_table = 'chart_html'

    style = EnumField()
    title = CharField(255)
    font_size = SmallIntegerField(default=26)
    title_color = IntegerField(default=0x000000)
    ken_burns = BooleanField(default=False)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        image_text_chart = super().from_dict(dictionary)
        image_text_chart.random = dictionary.get('random')
        image_text_chart.loop_limit = dictionary.get('loop_limit')
        image_text_chart.scale = dictionary.get('scale')
        image_text_chart.fullscreen = dictionary.get('fullscreen')
        image_text_chart.ken_burns = dictionary.get('ken_burns')
        image_text_chart.save()

        for text in dictionary.get('texts', tuple()):
            ChartText.add(image_text_chart, text)

        for image_id in dictionary.get('images', tuple()):
            ChartImage.add(image_text_chart, image_id)

        return image_text_chart

    @property
    def texts(self):
        """Yields appropriate texts."""
        return ChartText.select().where(ChartText.image_text_chart == self)

    @property
    def images(self):
        """Yields appropriate images."""
        return ChartImage.select().where(ChartImage.image_text_chart == self)

    def to_dict(self):
        """Returns a JSON compatible dictionary."""
        dictionary = super().to_dict()
        dictionary.update({
            'random': self.random,
            'loop_limit': self.loop_limit,
            'scale': self.scale,
            'fullscreen': self.fullscreen,
            'ken_burns': self.ken_burns,
            'texts': [text.text for text in self.texts],
            'images': [image.image for image in self.images]})
        return dictionary

    def delete_instance(recursive=False, delete_nullable=False):
        """Deletes related models and this model."""
        for text in self.texts:
            text.delete_instance()

        for image in self.images:
            image.delete_instance()

        super().delete_instance(
            recursive=recursive, delete_nullable=delete_nullable)


class ChartText(DSCMS4Model):
    """Text for an ImageTextChart."""

    class Meta:
        db_table = 'chart_text'

    image_text_chart = ForeignKeyField(
        ImageTextChart, db_column='image_text_chart')
    text = TextField()

    @classmethod
    def add(cls, image_text_chart, text):
        """Adds a new text for the respective ImageTextChart."""
        record = cls()
        record.image_text_chart = image_text_chart
        record.text = text
        record.save()
        return record


class ChartImage(DSCMS4Model):
    """Image for an ImageTextChart."""

    class Meta:
        db_table = 'chart_image'

    image_text_chart = ForeignKeyField(
        ImageTextChart, db_column='image_text_chart')
    image = IntegerField()
    bytes = FileProperty(image, file_client=FILE_CLIENT)

    @classmethod
    def add(cls, image_text_chart, image):
        """Adds a new image for the respective ImageTextChart."""
        record = cls()
        record.image_text_chart = image_text_chart
        record.image = image
        record.save()
        return record


class FacebookChart(Model, Chart):
    """Facebook data chart."""

    class Meta:
        db_table = 'chart_facebook'

    days = SmallIntegerField(default=14)
    limit = SmallIntegerField(default=10)
    facebook_id = CharField(255)
    facebook_name = CharField(255)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        chart = super().from_dict(dictionary)
        chart.days = dictionary.get('days')
        chart.limit = dictionary.get('limit')
        chart.facebook_id = dictionary.get('facebook_id')
        chart.facebook_name = dictionary.get('facebook_name')
        chart.save()
        return chart

    def to_dict(self):
        """Returns a JSON compatible dictionary."""
        dictionary = super.to_dict()
        dictionary.update({
            'days': self.days,
            'limit': self.limit,
            'facebook_id': self.facebook_id,
            'facebook_name': self.facebook_name})
        return dictionary


class GuessPictureChart(Model, Chart):
    """Chart for guessing pictures."""

    class Meta:
        db_table = 'chart_guess_picture'

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        chart = super().from_dict(dictionary)
        chart.save()
        return chart


class WeatherChart(Model, Chart):
    """Weather data."""

    class Meta:
        db_table = 'chart_weather'

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        chart = super().from_dict(dictionary)
        chart.save()
        return chart


MODELS = (
    BaseChart, LocalPublicTtransportChart, NewsChart, QuotesChart, VideoChart,
    ImageTextChart, ChartText, FacebookChart, GuessPictureChart, WeatherChart)
CHARTS = {
    model._meta.db_table.lstrip('chart_'): model
    for model in MODELS if issubclass(model, Chart)}
