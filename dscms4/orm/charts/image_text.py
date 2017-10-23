"""Image / text charts."""

from enum import Enum

from peewee import Model, ForeignKeyField, IntegerField, SmallIntegerField, \
    BooleanField, CharField, TextField

from peeweeplus import EnumField

from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model
from dscms4.orm.media import MediaFile


class Style(Enum):
    """Chart styles."""

    DEFAULT = 'default'
    PIN_CHART = 'pin chart'


class ImageTextChart(Model, Chart):
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
        image_text_chart = super().from_dict(dictionary)
        image_text_chart.random = dictionary.get('random')
        image_text_chart.loop_limit = dictionary.get('loop_limit')
        image_text_chart.scale = dictionary.get('scale')
        image_text_chart.fullscreen = dictionary.get('fullscreen')
        image_text_chart.ken_burns = dictionary.get('ken_burns')
        image_text_chart.save()

        for text in dictionary.get('texts', tuple()):
            ImageTextChartText.add(image_text_chart, text)

        for image_id in dictionary.get('images', tuple()):
            ImageTextChartImage.add(image_text_chart, image_id)

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
    def add(cls, image_text_chart, image):
        """Adds a new image for the respective ImageTextChart."""
        record = cls()
        record.image_text_chart = image_text_chart
        record.image = image
        record.save()
        return record
