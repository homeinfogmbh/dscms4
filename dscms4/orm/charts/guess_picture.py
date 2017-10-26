"""Oicture guessing chart."""

from peewee import Model
from dscms4.orm.charts.common import Chart

__all__ = ['GuessPicture']


class GuessPicture(Model, Chart):
    """Chart for guessing pictures."""

    class Meta:
        db_table = 'chart_guess_picture'

    @classmethod
    def from_dict(cls, dictionary):
        """Yields the chart."""
        yield super().from_dict(dictionary)