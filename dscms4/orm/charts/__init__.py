"""Chart ORM models.

This package provides ORM models
of the "chart" types of the CMS.
"""
from dscms4.orm.charts.common import ChartGroup, BaseChart, Chart
from dscms4.orm.charts.facebook import Facebook, Account
from dscms4.orm.charts.form import Form
from dscms4.orm.charts.guess_picture import GuessPicture
from dscms4.orm.charts.image_text import ImageText, Image, Text
from dscms4.orm.charts.news import News
from dscms4.orm.charts.public_transport import PublicTransport
from dscms4.orm.charts.quotes import Quotes
from dscms4.orm.charts.video import Video
from dscms4.orm.charts.weather import Weather


__all__ = ['MODELS', 'CHARTS']


MODELS = (
    BaseChart, Facebook, Form, Account, GuessPicture, ImageText, Image, Text,
    News, PublicTransport, Quotes, Video, Weather)
CHARTS = {
    model.__name__: model for model in MODELS if issubclass(model, Chart)}


print('Known chart types:', ', '.join(CHARTS), flush=True)
