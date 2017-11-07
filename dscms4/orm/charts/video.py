"""Video charts."""

from peewee import Model, ForeignKeyField

from dscms4.orm.charts.common import Chart
from dscms4.orm.media import MediaFile

__all__ = ['Video']


class Video(Model, Chart):
    """A chart that may contain images and texts."""

    class Meta:
        db_table = 'chart_video'

    video = ForeignKeyField(
        MediaFile, db_column='video', null=True, default=None)

    @classmethod
    def from_dict(cls, dictionary):
        """Creates a new quotes chart from the
        dictionary for the respective customer.
        """
        chart = super().from_dict(dictionary)
        chart.video = dictionary['video']
        return chart

    @property
    def dictionary(self):
        """Returns a JSON-ish dictionary."""
        return {'video': self.video.id}
