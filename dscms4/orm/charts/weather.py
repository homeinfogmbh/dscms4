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
    JSON_KEYS = {
        'fontColor': font_color, 'iconColor': icon_color,
        'boxColorTop': box_color_top, 'boxColorMiddle': box_color_middle,
        'boxColorBottom': box_color_bottom}

    @classmethod
    def from_json(cls, customer, dictionary, **kwargs):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        # Pop images and texts first to exclude them from the
        # dictionary before invoking super().from_json().
        images = dictionary.pop('images', ())
        transaction = super().from_json(customer, dictionary, **kwargs)

        for image in images:
            image = Image.add(transaction.chart, image)
            transaction.add(image)

        return transaction

    @property
    def files(self):
        """Returns a set of IDs of files used by the chart."""
        files = set()

        for image in self.images:
            files.add(image.image)

        return files

    def patch_json(self, json, **kwargs):
        """Patches the respective chart."""
        images = json.pop('images', _UNCHANGED) or ()
        transaction = super().patch_json(json, **kwargs)

        if images is not _UNCHANGED:
            for image in self.images:
                transaction.delete(image)

            for image in images:
                image = Image.add(transaction.chart, image)
                transaction.add(image)

        return transaction

    def to_json(self, brief=False, **kwargs):
        """Returns the dictionary representation of this chart's fields."""
        json = super().to_json(brief=brief, **kwargs)

        if not brief:
            json['images'] = [image.image for image in self.images]

        return json

    def to_dom(self, brief=False):
        """Returns an XML DOM of this chart."""
        if brief:
            return super().to_dom(dom.BriefChart)

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
