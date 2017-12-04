"""Video charts."""

from peewee import ForeignKeyField

from dscms4.orm.charts.common import Chart
from dscms4.orm.common DSCMS4Model
from dscms4.orm.media import MediaFile

__all__ = ['Video']


class Video(DSCMS4Model, Chart):
    """A chart that may contain images and texts."""

    class Meta:
        db_table = 'chart_video'

    video = ForeignKeyField(
        MediaFile, db_column='video', null=True, default=None)
