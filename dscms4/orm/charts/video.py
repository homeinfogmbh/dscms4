"""Video charts."""

from peewee import IntegerField

from functoolsplus import coerce

from dscms4 import dom
from dscms4.domutil import attachment_dom
from dscms4.orm.charts.common import Chart, RegisteredChart


__all__ = ['Video']


class Video(Chart, metaclass=RegisteredChart):
    """A chart that may contain images and texts."""

    class Meta:
        table_name = 'chart_video'

    video = IntegerField(null=True)

    @property
    @coerce(set)
    def files(self):
        """Returns a set of IDs of files used by the chart."""
        if self.video is not None:
            yield self.video

    def to_dom(self, brief=False):
        """Returns an XML DOM of this chart."""
        if brief:
            return super().to_dom(dom.BriefChart)

        xml = super().to_dom(dom.Video)
        xml.video = attachment_dom(self.video)
        return xml
