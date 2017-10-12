"""Object Relational Mappings"""

from datetime import datetime
from enum import Enum
from sys import stderr

from peewee import Model, ForeignKeyField, CharField, TextField, \
    DateTimeField, BooleanField, IntegerField, SmallIntegerField

from filedb import FileProperty, FileClient
from peeweeplus import EnumField

from .common import DSCMS4Model, CustomerModel
from .exceptions import OrphanedBaseChart
from .schedule import Schedule
# from .exceptions import InvalidData, MissingData


__all__ = ['Chart']

DEFAULT_DURATION = 10


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
        for _, cls in CHARTS.items():
            with suppress(DoesNotExist):
                return cls.get(cls.base_chart == self)

        raise OrphanedBaseChart(self)

    def to_dict(self):
        """Returns a JSON compatible dictionary."""
        dictionary = super().to_dict()
        dictionary.update({
            'title': self.title,
            'description': self.description,
            'duration': self.duration,
            'created': self.created.isoformat(),
            'transition_effect': self.transition_effect.value})

        if self.schedule:
            dictionary['schedule'] = self.schedule.to_dict()
        else:
            dictionary['schedule'] = None

        return dictionary


class Chart(DSCMS4Model):
    """Abstract basic chart."""

    base_chart = ForeignKeyField(BaseChart, db_column='base_chart')

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new chart from the respective dictionary."""
        chart = cls()
        chart.base_chart = BaseChart.from_dict(dictionary['base_chart'])
        return chart

    def to_dict(self, cascade=False):
        """Converts the chart into a JSON compliant dictionary."""
        dictionary = super().to_dict()
        dictionary['base_chart'] = self.base_chart.to_dict()
        return dictionary


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
        chart.file = dictionary['file']
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
    def chart_texts(self):
        """Yields appropriate texts."""
        return ChartText.select().where(ChartText.image_text_chart == self)

    @property
    def chart_images(self):
        """Yields appropriate images."""
        return ChartImage.select().where(ChartImage.image_text_chart == self)

    def _to_dict(self):
        """Returns the dictionary representation of this chart's fields."""
        return {
            'random': self.random,
            'loop_limit': self.loop_limit,
            'scale': self.scale,
            'fullscreen': self.fullscreen,
            'ken_burns': self.ken_burns,
            'texts': [chart_text.text for chart_text in self.chart_texts],
            'images': [chart_image.image for chart_image in self.chart_images]}

    def to_dict(self):
        """Returns a JSON compatible dictionary."""
        dictionary = super().to_dict()
        dictionary.update(self._to_dict())
        return dictionary

    def delete_instance(self, recursive=False, delete_nullable=False):
        """Deletes related models and this model."""
        for chart_text in self.chart_texts:
            chart_text.delete_instance()

        for chart_image in self.chart_images:
            chart_image.delete_instance()

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
    file = IntegerField()
    image = FileProperty(image, file_client=FILE_CLIENT)

    @classmethod
    def add(cls, image_text_chart, file):
        """Adds a new image for the respective ImageTextChart."""
        record = cls()
        record.image_text_chart = image_text_chart
        record.file = file
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

    def _to_dict(self):
        """Returns a JSON compliant dictionary of this chart's fields."""
        return {
            'days': self.days,
            'limit': self.limit,
            'facebook_id': self.facebook_id,
            'facebook_name': self.facebook_name}

    def to_dict(self):
        """Returns a JSON compatible dictionary."""
        dictionary = super.to_dict()
        dictionary.update(self._to_dict())
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
