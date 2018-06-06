"""Image / text charts."""

from enum import Enum

from peewee import ForeignKeyField, IntegerField, SmallIntegerField, \
    BooleanField, CharField, TextField

from peeweeplus import EnumField

from dscms4 import dom
from dscms4.domutil import attachment_dom
from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model

__all__ = ['ImageText', 'Image', 'Text']


_UNCHANGED = object()


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

    def patch(self, dictionary, **kwargs):
        """Patches the respective chart."""
        images = dictionary.pop('images', _UNCHANGED) or ()
        texts = dictionary.pop('texts', _UNCHANGED) or ()
        base, chart = super().patch(dictionary, **kwargs)
        yield base
        yield chart

        if images is not _UNCHANGED:
            for image in self.images:
                image.delete_instance()

            for image in images:
                yield Image.add(chart, image)

        if texts is not _UNCHANGED:
            for text in self.texts:
                text.delete_instance()

            for text in texts:
                yield Text.add(chart, text)

    def to_dict(self, *args, brief=False, **kwargs):
        """Returns the dictionary representation of this chart's fields."""
        dictionary = super().to_dict(*args, brief=brief, **kwargs)

        if not brief:
            dictionary['texts'] = [text.text for text in self.texts]
            dictionary['images'] = [image.image for image in self.images]

        return dictionary

    def to_dom(self):
        """Returns an XML DOM of this chart."""
        xml = super().to_dom(dom.ImageText)
        xml.style = self.style.value
        xml.title = self.title
        xml.font_size = self.font_size
        xml.title_color = self.title_color
        xml.ken_burns = self.ken_burns
        xml.image = [image.to_dom() for image in self.images]
        xml.text = [text.text for text in self.texts]
        return xml


class Image(DSCMS4Model):
    """Image for an ImageText chart."""

    class Meta:
        table_name = 'chart_image_text_image'

    chart = ForeignKeyField(
        ImageText, column_name='chart', backref='images', on_delete='CASCADE')
    image = IntegerField()

    @classmethod
    def add(cls, chart, image):
        """Adds a new image for the respective ImageText chart."""
        record = cls()
        record.chart = chart
        record.image = image
        return record

    def to_dom(self):
        """Returns an XML DOM of this model."""
        return attachment_dom(self.image)


class Text(DSCMS4Model):
    """Text for an ImageText chart."""

    class Meta:
        table_name = 'chart_image_text_text'

    chart = ForeignKeyField(
        ImageText, column_name='chart', backref='texts', on_delete='CASCADE')
    text = TextField()

    @classmethod
    def add(cls, chart, text):
        """Adds a new text for the respective ImageText chart."""
        record = cls()
        record.chart = chart
        record.text = text
        return record
