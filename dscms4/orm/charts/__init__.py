"""Chart ORM models.

This package provides ORM models
of the "chart" types of the CMS.
"""
from sys import stderr

from dscms4.orm.charts.common import BaseChart, Chart
from dscms4.orm.charts.facebook import Facebook, Account
from dscms4.orm.charts.guess_picture import GuessPicture
from dscms4.orm.charts.image_text import ImageText, Image, Text
from dscms4.orm.charts.news import News
from dscms4.orm.charts.public_transport import PublicTransport
from dscms4.orm.charts.quotes import Quotes
from dscms4.orm.charts.video import Video
from dscms4.orm.charts.weather import Weather


__all__ = ['MODELS', 'CHARTS', 'create_tables']


MODELS = (
    BaseChart, Facebook, Account, GuessPicture, ImageText, Image, Text, News,
    PublicTransport, Quotes, Video, Weather)
CHARTS = {
    model._meta.db_table.lstrip('chart_'): model
    for model in MODELS if issubclass(model, Chart)}


def create_tables(fail_silently=True):
    """Create the respective tables."""

    for model in MODELS:
        try:
            model.create_table(fail_silently=fail_silently)
        except Exception:
            print('Could not create table for model "{}".'.format(model),
                  file=stderr)
