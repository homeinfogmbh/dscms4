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
    def from_dict(cls, customer, dictionary, schedule=None):
        """Creates a base chart from a dictionary
        for the respective customer.
        """
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
            dictionary['schedule'] = self.schedule.id
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
        dictionary['base_chart'] = self.base_chart.id
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

    video = ForeignKeyField(
        MediaFile, db_column='video', null=True, default=None)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        chart = super().from_dict(dictionary)
        chart.video = dictionary['video']
        chart.save()
        return chart

    def to_dict(self):
        """Returns a JSON compatible dictionary"""
        dictionary = super().to_dict()
        dictionary['video'] = self.video.id
        return dictionary


class ImageTextChart(Model, Chart):
    """A chart that may contain images and text."""

    class Meta:
        db_table = 'chart_image_text'

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
    def image_text_chart_texts(self):
        """Yields appropriate text mappings."""
        return ImageTextChartText.select().where(
            ImageTextChartText.image_text_chart == self)

    @property
    def image_text_chart_images(self):
        """Yields appropriate image mappings."""
        return ImageTextChartImage.select().where(
            ImageTextChartImage.image_text_chart == self)

    @property
    def texts(self):
        """Yields appropriate texts."""
        for image_text_chart_text in self.image_text_chart_texts:
            yield image_text_chart_text.text

    @property
    def images(self):
        """Yields appropriate images."""
        for image_text_chart_image in self.image_text_chart_images:
            yield image_text_chart_image.image

    @property
    def dictionary(self):
        """Returns the dictionary representation of this chart's fields."""
        return {
            'random': self.random,
            'loop_limit': self.loop_limit,
            'scale': self.scale,
            'fullscreen': self.fullscreen,
            'ken_burns': self.ken_burns,
            'texts': list(self.texts),
            'images': list(self.images)}

    def to_dict(self):
        """Returns a JSON compatible dictionary."""
        dictionary = super().to_dict()
        dictionary.update(self.dictionary)
        return dictionary

    def delete_instance(self, recursive=False, delete_nullable=False):
        """Deletes related models and this model."""
        for chart_text in self.chart_texts:
            chart_text.delete_instance()

        for chart_image in self.chart_images:
            chart_image.delete_instance()

        super().delete_instance(
            recursive=recursive, delete_nullable=delete_nullable)


class ImageTextChartText(DSCMS4Model):
    """Text for an ImageTextChart."""

    class Meta:
        db_table = 'chart_image_text_text'

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


class ImageTextChartImage(DSCMS4Model):
    """Image for an ImageTextChart."""

    class Meta:
        db_table = 'chart_image_text_image'

    image_text_chart = ForeignKeyField(
        ImageTextChart, db_column='image_text_chart')
    image = ForeignKeyField(MediaFile, db_column='image')

    @classmethod
    def add(cls, image_text_chart, media_file):
        """Adds a new image for the respective ImageTextChart."""
        record = cls()
        record.image_text_chart = image_text_chart
        record.file = media_file
        record.save()
        return record


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
