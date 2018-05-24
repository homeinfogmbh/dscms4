"""Video charts."""

from peewee import IntegerField

from dscms4.orm.charts.common import Chart

__all__ = ['Video']


class Video(Chart):
    """A chart that may contain images and texts."""

    class Meta:
        table_name = 'chart_video'

    video = IntegerField()
