"""Weather chart."""

from peewee import ForeignKeyField, IntegerField, CharField

from dscms4 import dom
from dscms4.domutil import attachment_dom
from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model

__all__ = ['Weather', 'Image']


_UNCHANGED = object()


class Weather(Chart):
    """Weather data."""

    class Meta:
        table_name = 'chart_weather'

    location = CharField(255)
    font_color = IntegerField()
    icon_color = IntegerField()
    box_color_top = IntegerField()
    box_color_middle = IntegerField()
    box_color_bottom = IntegerField()
    transparency = IntegerField()

    @classmethod
    def from_dict(cls, customer, dictionary, **kwargs):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        # Pop images and texts first to exclude them from the
        # dictionary before invoking super().from_dict().
        images = dictionary.pop('images', ())
        base, chart = super().from_dict(customer, dictionary, **kwargs)
        yield base
        yield chart

        for image in images:
            yield Image.add(chart, image)

    def patch(self, dictionary, **kwargs):
        """Patches the respective chart."""
        images = dictionary.pop('images', _UNCHANGED) or ()
        base, chart = super().patch(dictionary, **kwargs)
        yield base
        yield chart

        if images is not _UNCHANGED:
            for image in self.images:
                image.delete_instance()

            for image in images:
                yield Image.add(chart, image)

    def to_dict(self, *args, brief=False, **kwargs):
        """Returns the dictionary representation of this chart's fields."""
        dictionary = super().to_dict(*args, brief=brief, **kwargs)

        if not brief:
            dictionary['images'] = [image.image for image in self.images]

        return dictionary

    def to_dom(self):
        """Returns an XML DOM of this chart."""
        xml = super().to_dom(dom.Weather)
        xml.location = self.location
        xml.font_color = self.font_color
        xml.icon_color = self.icon_color
        xml.box_color_top = self.box_color_top
        xml.box_color_middle = self.box_color_middle
        xml.box_color_bottom = self.box_color_bottom
        xml.transparency = self.transparency
        xml.image = list(filter(None, (img.to_dom() for img in self.images)))
        return xml


class Image(DSCMS4Model):
    """Image for an ImageTextChart."""

    class Meta:
        table_name = 'chart_weather_image'

    chart = ForeignKeyField(
        Weather, column_name='chart', backref='images', on_delete='CASCADE')
    image = IntegerField()

    @classmethod
    def add(cls, chart, image):
        """Adds a new image for the respective Weather chart."""
        record = cls()
        record.chart = chart
        record.image = image
        return record

    def to_dom(self):
        """Returns an XML DOM of this model."""
        return attachment_dom(self.image)
