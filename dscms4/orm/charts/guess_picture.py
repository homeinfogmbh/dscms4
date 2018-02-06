"""Oicture guessing chart."""

from dscms4.orm.charts.common import Chart

__all__ = ['GuessPicture']


class GuessPicture(Chart):
    """Chart for guessing pictures."""

    class Meta:
        table_name = 'chart_guess_picture'
