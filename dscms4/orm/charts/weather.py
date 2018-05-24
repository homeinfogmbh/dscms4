"""Weather chart."""

from peewee import ForeignKeyField, IntegerField, CharField

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

    @property
    def images(self):
        """Yields appropriate image mappings."""
        return Image.select().where(Image.chart == self)

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

    def to_dict(self, *args, base_chart=True, type_=True, **kwargs):
        """Returns the dictionary representation of this chart's fields."""
        dictionary = super().to_dict(
            *args, base_chart=base_chart, type_=type_, **kwargs)
        dictionary['images'] = [image.image for image in self.images]
        return dictionary


class Image(DSCMS4Model):
    """Image for an ImageTextChart."""

    class Meta:
        table_name = 'chart_weather_image'

    chart = ForeignKeyField(Weather, column_name='chart', on_delete='CASCADE')
    image = IntegerField()

    @classmethod
    def add(cls, chart, image):
        """Adds a new image for the respective Weather chart."""
        record = cls()
        record.chart = chart
        record.image = image
        return record
