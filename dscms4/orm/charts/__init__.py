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

from dscms4.orm.exceptions import OrphanedBaseChart, AmbiguousBaseChart


__all__ = [
    'MODELS',
    'CHARTS',
    'create_tables',
    'charts_of',
    'chart_of']


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


def charts_of(base_chart):
    """Yields all charts that associate this base chart."""

    for _, cls in CHARTS.items():
        yield from cls.select().where(cls.base_chart == base_chart)


def chart_of(base_chart):
    """Returns the mapped implementation of the respective base chart."""

    try:
        match, *superfluous = charts_of(base_chart)
    except ValueError:
        raise OrphanedBaseChart(base_chart)

    if superfluous:
        raise AmbiguousBaseChart(base_chart, [match] + superfluous)

    return match
