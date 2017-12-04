"""Oicture guessing chart."""

from dscms4.orm.charts.common import Chart
from dscms4.orm.common import DSCMS4Model

__all__ = ['GuessPicture']


class GuessPicture(DSCMS4Model, Chart):
    """Chart for guessing pictures."""

    class Meta:
        db_table = 'chart_guess_picture'
