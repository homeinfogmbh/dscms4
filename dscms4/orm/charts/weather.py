"""Weather chart."""

from peewee import ForeignKeyField, IntegerField, CharField

from functoolsplus import coerce

from dscms4 import dom
from dscms4.domutil import attachment_dom
from dscms4.orm.charts.common import ChartMode, Chart
from dscms4.orm.common import UNCHANGED, DSCMS4Model


__all__ = ['Weather', 'Image']


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
    def from_json(cls, json, **kwargs):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        # Pop images and texts first to exclude them from the
        # dictionary before invoking super().from_json().
        images = json.pop('images', ())
        transaction = super().from_json(json, **kwargs)

        for image in images:
            image = Image(chart=transaction.chart, image=image)
            transaction.add(image)

        return transaction

    @property
    @coerce(set)
    def files(self):
        """Returns a set of IDs of files used by the chart."""
        for image in self.images:
            yield image.image

    def patch_json(self, json, **kwargs):
        """Patches the respective chart."""
        images = json.pop('images', UNCHANGED) or ()
        transaction = super().patch_json(json, **kwargs)

        if images is not UNCHANGED:
            for image in self.images:
                transaction.delete(image)

            for image in images:
                image = Image(chart=transaction.chart, image=image)
                transaction.add(image)

        return transaction

    def to_json(self, mode=ChartMode.FULL, **kwargs):
        """Returns the dictionary representation of this chart's fields."""
        json = super().to_json(mode=mode, **kwargs)

        if mode == ChartMode.FULL:
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

    def to_dom(self):
        """Returns an XML DOM of this model."""
        return attachment_dom(self.image)
