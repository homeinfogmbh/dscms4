"""Video charts."""

from peewee import IntegerField

from dscms4 import dom
from dscms4.domutil import attachment_dom
from dscms4.orm.charts.common import Chart

__all__ = ['Video']


class Video(Chart):
    """A chart that may contain images and texts."""

    class Meta:
        table_name = 'chart_video'

    video = IntegerField(null=True)

    @property
    def files(self):
        """Yields the file IDs used by the chart."""
        return {self.video}

    def to_dom(self, brief=False):
        """Returns an XML DOM of this chart."""
        if brief:
            return super().to_dom(dom.BriefChart)

        xml = super().to_dom(dom.Video)
        xml.video = attachment_dom(self.video)
        return xml
