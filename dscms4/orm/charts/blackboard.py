"""Black board charts."""

from enum import Enum

from peewee import ForeignKeyField
from peewee import IntegerField

from functoolsplus import coerce
from peeweeplus import EnumField

from dscms4 import dom
from dscms4.domutil import attachment_dom
from dscms4.orm.charts.common import ChartMode, Chart
from dscms4.orm.common import UNCHANGED, DSCMS4Model


__all__ = ['Blackboard', 'Image']


class Format(Enum):
    """Image display format."""

    A4 = 'A4'
    A5 = 'A5'
    A6 = 'A6'


class Blackboard(Chart):
    """A chart that may contain images and text."""

    class Meta:
        table_name = 'chart_blackboard'

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

        xml = super().to_dom(dom.ImageText)
        xml.image = list(filter(None, (img.to_dom() for img in self.images)))
        return xml


class Image(DSCMS4Model):
    """Image for an ImageText chart."""

    class Meta:
        table_name = 'chart_blackboard_image'

    chart = ForeignKeyField(
        Blackboard, column_name='chart', backref='images', on_delete='CASCADE')
    image = IntegerField()
    format = EnumField(Format, default=Format.A4)

    def to_dom(self):
        """Returns an XML DOM of this model."""
        return attachment_dom(self.image)
