"""Image / text charts."""

from enum import Enum

from peewee import Model, ForeignKeyField, IntegerField, SmallIntegerField, \
    BooleanField, CharField, TextField

from peeweeplus import EnumField

from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model
from dscms4.orm.media import MediaFile

__all__ = ['ImageText', 'Image', 'Text']


class Style(Enum):
    """Chart styles."""

    DEFAULT = 'default'
    PIN_CHART = 'pin chart'


class ImageText(Model, Chart):
    """A chart that may contain images and text."""

    class Meta:
        db_table = 'chart_image_text'

    style = EnumField(Style)
    title = CharField(255)
    font_size = SmallIntegerField(default=26)
    title_color = IntegerField(default=0x000000)
    ken_burns = BooleanField(default=False)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        chart = super().from_dict(dictionary)
        chart.style = dictionary.get('style')
        chart.title = dictionary.get('title')
        chart.font_size = dictionary.get('font_size')
        chart.title_color = dictionary.get('title_color')
        chart.ken_burns = dictionary.get('ken_burns')
        yield chart

        for image_id in dictionary.get('images', ()):
            yield Image.add(chart, image_id)

        for text in dictionary.get('texts', ()):
            yield Text.add(chart, text)

    @property
    def image_models(self):
        """Yields appropriate image mappings."""
        return Image.select().where(Image.chart == self)

    @property
    def text_models(self):
        """Yields appropriate text mappings."""
        return Text.select().where(Text.chart == self)

    @property
    def images(self):
        """Yields appropriate images."""
        for image_model in self.image_models:
            yield image_model.image

    @property
    def texts(self):
        """Yields appropriate texts."""
        for text_model in self.text_models:
            yield text_model.text

    @property
    def dictionary(self):
        """Returns the dictionary representation of this chart's fields."""
        return {
            'random': self.random,
            'loop_limit': self.loop_limit,
            'scale': self.scale,
            'fullscreen': self.fullscreen,
            'ken_burns': self.ken_burns,
            'texts': tuple(self.texts),
            'images': tuple(self.images)}

    def delete_instance(self, recursive=False, delete_nullable=False):
        """Deletes related models and this model."""
        for chart_text in self.chart_texts:
            chart_text.delete_instance()

        for chart_image in self.chart_images:
            chart_image.delete_instance()

        super().delete_instance(
            recursive=recursive, delete_nullable=delete_nullable)


class Image(Model, DSCMS4Model):
    """Image for an ImageTextChart."""

    class Meta:
        db_table = 'chart_image_text_image'

    chart = ForeignKeyField(ImageText, db_column='image_text_chart')
    image = ForeignKeyField(MediaFile, db_column='image')

    @classmethod
    def add(cls, chart, image):
        """Adds a new image for the respective ImageTextChart."""
        record = cls()
        record.chart = chart
        record.image = image
        return record


class Text(Model, DSCMS4Model):
    """Text for an ImageTextChart."""

    class Meta:
        db_table = 'chart_image_text_text'

    chart = ForeignKeyField(ImageText, db_column='image_text_chart')
    text = TextField()

    @classmethod
    def add(cls, chart, text):
        """Adds a new text for the respective ImageTextChart."""
        record = cls()
        record.chart = chart
        record.text = text
        return record
