"""Image / text charts."""

from enum import Enum

from peewee import ForeignKeyField, IntegerField, SmallIntegerField, \
    BooleanField, CharField, TextField
from peeweeplus import EnumField

from hisfs.orm import File

from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model

__all__ = ['ImageText', 'Image', 'Text']


class Style(Enum):
    """Chart styles."""

    DEFAULT = 'default'
    PIN_CHART = 'pin chart'


class ImageText(Chart):
    """A chart that may contain images and text."""

    class Meta:
        table_name = 'chart_image_text'

    style = EnumField(Style)
    title = CharField(255)
    font_size = SmallIntegerField(default=26)
    title_color = IntegerField(default=0x000000)
    ken_burns = BooleanField(default=False)

    @classmethod
    def from_dict(cls, customer, dictionary, **kwargs):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        # Pop images and texts first to exclude them from the
        # dictionary before invoking super().from_dict().
        images = dictionary.pop('images', ())
        texts = dictionary.pop('texts', ())
        base, chart = super().from_dict(customer, dictionary, **kwargs)
        yield base
        yield chart

        for image in images:
            yield Image.add(chart, image)

        for text in texts:
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

    def to_dict(self):
        """Returns the dictionary representation of this chart's fields."""
        dictionary = super().to_dict()
        dictionary['texts'] = tuple(self.texts)
        dictionary['images'] = tuple(self.images)
        return dictionary


class Image(DSCMS4Model):
    """Image for an ImageTextChart."""

    class Meta:
        table_name = 'chart_image_text_image'

    chart = ForeignKeyField(
        ImageText, column_name='chart', on_delete='CASCADE')
    image = ForeignKeyField(File, column_name='image', on_delete='CASCADE')

    @classmethod
    def add(cls, chart, image):
        """Adds a new image for the respective ImageTextChart."""
        record = cls()
        record.chart = chart
        record.image = image
        return record


class Text(DSCMS4Model):
    """Text for an ImageTextChart."""

    class Meta:
        table_name = 'chart_image_text_text'

    chart = ForeignKeyField(
        ImageText, column_name='chart', on_delete='CASCADE')
    text = TextField()

    @classmethod
    def add(cls, chart, text):
        """Adds a new text for the respective ImageTextChart."""
        record = cls()
        record.chart = chart
        record.text = text
        return record
