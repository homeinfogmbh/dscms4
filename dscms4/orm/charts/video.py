"""Video charts."""

from peewee import ForeignKeyField

from dscms4.orm.charts.common import Chart
from dscms4.orm.file import File

__all__ = ['Video']


class Video(Chart):
    """A chart that may contain images and texts."""

    class Meta:
        table_name = 'chart_video'

    video = ForeignKeyField(File, column_name='video', on_delete='CASCADE')
