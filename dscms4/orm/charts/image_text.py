"""Image / text charts."""

from peewee import BooleanField
from peewee import CharField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import SmallIntegerField
from peewee import TextField

from dscms4 import dom
from dscms4.domutil import attachment_dom
from dscms4.orm.charts.common import ChartMode, Chart
from dscms4.orm.common import UNCHANGED, DSCMS4Model


__all__ = ['ImageText', 'Image', 'Text']


class ImageText(Chart):
    """A chart that may contain images and text."""

    class Meta:
        table_name = 'chart_image_text'

    title = CharField(255)
    font_size = SmallIntegerField(default=26)
    title_color = IntegerField(default=0x000000)
    ken_burns = BooleanField(default=False)

    @classmethod
    def from_json(cls, json, **kwargs):
        """Creates a new chart from a JSON-ish dict."""
        # Pop images and texts first to exclude them from the
        # dictionary before invoking super().from_json().
        images = json.pop('images', ())
        texts = json.pop('texts', ())
        transaction = super().from_json(json, **kwargs)

        for image in images:
            image = Image(chart=transaction.chart, image=image)
            transaction.add(image)

        for text in texts:
            text = Text(chart=transaction.chart, text=text)
            transaction.add(text)

        return transaction

    @property
    def files(self):
        """Returns a set of IDs of files used by the chart."""
        return set(image.image for image in self.images)

    def patch_json(self, json, **kwargs):
        """Patches the respective chart."""
        images = json.pop('images', UNCHANGED) or ()
        texts = json.pop('texts', UNCHANGED) or ()
        transaction = super().patch_json(json, **kwargs)

        if images is not UNCHANGED:
            for image in self.images:
                transaction.delete(image)

            for image in images:
                image = Image(chart=transaction.chart, image=image)
                transaction.add(image)

        if texts is not UNCHANGED:
            for text in self.texts:
                transaction.delete(text)

            for text in texts:
                text = Text(chart=transaction.chart, text=text)
                transaction.add(text)

        return transaction

    def to_json(self, mode=ChartMode.FULL, **kwargs):
        """Returns the dictionary representation of this chart's fields."""
        json = super().to_json(mode=mode, **kwargs)

        if mode == ChartMode.FULL:
            json['texts'] = [text.text for text in self.texts]
            json['images'] = [
                image.to_json(fk_fields=False, autofields=False)
                for image in self.images.order_by(Image.index)]

        return json

    def to_dom(self, brief=False):
        """Returns an XML DOM of this chart."""
        if brief:
            return super().to_dom(dom.BriefChart)

        xml = super().to_dom(dom.ImageText)
        xml.title = self.title
        xml.font_size = self.font_size
        xml.title_color = self.title_color
        xml.ken_burns = self.ken_burns
        xml.image = filter(None, (
            image.to_dom() for image in self.images.order_by(Image.index)))
        xml.text = [text.text for text in self.texts]
        return xml


class Image(DSCMS4Model):
    """Image for an ImageText chart."""

    class Meta:
        table_name = 'chart_image_text_image'

    chart = ForeignKeyField(
        ImageText, column_name='chart', backref='images', on_delete='CASCADE')
    image = IntegerField()
    index = IntegerField(default=0)

    def to_dom(self):
        """Returns an XML DOM of this model."""
        return attachment_dom(self.image, index=self.index)


class Text(DSCMS4Model):
    """Text for an ImageText chart."""

    class Meta:
        table_name = 'chart_image_text_text'

    chart = ForeignKeyField(
        ImageText, column_name='chart', backref='texts', on_delete='CASCADE')
    text = TextField()
