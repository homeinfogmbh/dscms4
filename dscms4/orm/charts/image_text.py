"""Image / text charts."""

from enum import Enum

from peewee import ForeignKeyField, IntegerField, SmallIntegerField, \
    BooleanField, CharField, TextField

from peeweeplus import EnumField

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

    @property
    def images(self):
        """Yields appropriate image mappings."""
        return Image.select().where(Image.chart == self)

    @property
    def texts(self):
        """Yields appropriate text mappings."""
        return Text.select().where(Text.chart == self)

    def patch(self, dictionary, **kwargs):
        """Patches the respective chart."""
        images = dictionary.pop('images', _UNCHANGED) or ()
        texts = dictionary.pop('texts', _UNCHANGED) or ()
        base, chart = super().patch(dictionary, **kwargs)
        yield base
        yield chart

        try:
            images = dictionary.pop('images') or ()
        except KeyError:
            pass
        else:
            for image in self.images:
                image.delete_instance()

            for image in images:
                yield Image.add(chart, image)

        try:
            texts = dictionary.pop('texts') or ()
        except KeyError:
            pass
        else:
            for text in self.texts:
                text.delete_instance()

            for text in texts:
                yield Text.add(chart, text)

    def to_dict(self, *args, base_chart=True, type_=True, **kwargs):
        """Returns the dictionary representation of this chart's fields."""
        dictionary = super().to_dict(
            *args, base_chart=base_chart, type_=type_, **kwargs)
        dictionary['texts'] = [text.text for text in self.texts]
        dictionary['images'] = [image.id for image in self.images]
        return dictionary


class Image(DSCMS4Model):
    """Image for an ImageText chart."""

    class Meta:
        table_name = 'chart_image_text_image'

    chart = ForeignKeyField(
        ImageText, column_name='chart', on_delete='CASCADE')
    image = IntegerField()

    @classmethod
    def add(cls, chart, image):
        """Adds a new image for the respective ImageText chart."""
        record = cls()
        record.chart = chart
        record.image = image
        return record


class Text(DSCMS4Model):
    """Text for an ImageText chart."""

    class Meta:
        table_name = 'chart_image_text_text'

    chart = ForeignKeyField(
        ImageText, column_name='chart', on_delete='CASCADE')
    text = TextField()

    @classmethod
    def add(cls, chart, text):
        """Adds a new text for the respective ImageText chart."""
        record = cls()
        record.chart = chart
        record.text = text
        return record
