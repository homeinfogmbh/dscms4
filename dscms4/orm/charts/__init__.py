"""Chart ORM models.

This package provides ORM models
of the "chart" types of the CMS.
"""
from dscms4.orm.charts.blackboard import Blackboard, Image as BlackboardImage
from dscms4.orm.charts.cleaning import Cleaning
from dscms4.orm.charts.common import ChartMode, BaseChart, Chart
from dscms4.orm.charts.facebook import Facebook, Account
from dscms4.orm.charts.form import Form
from dscms4.orm.charts.garbage_collection import GarbageCollection
from dscms4.orm.charts.guess_picture import GuessPicture
from dscms4.orm.charts.image_text import ImageText
from dscms4.orm.charts.image_text import Image as ImageTextImage
from dscms4.orm.charts.image_text import Text
from dscms4.orm.charts.news import News
from dscms4.orm.charts.public_transport import PublicTransport
from dscms4.orm.charts.quotes import Quotes
from dscms4.orm.charts.real_estates import RealEstates
from dscms4.orm.charts.real_estates import IdFilter
from dscms4.orm.charts.real_estates import ZipCodeFilter
from dscms4.orm.charts.video import Video
from dscms4.orm.charts.weather import Weather, Image as WeatherImage


__all__ = ['MODELS', 'ChartMode', 'BaseChart', 'Chart']


MODELS = (
    BaseChart, Cleaning, Facebook, Account, Form, GarbageCollection,
    GuessPicture, ImageText, ImageTextImage, Blackboard, BlackboardImage, Text,
    News, PublicTransport, Quotes, RealEstates, IdFilter, ZipCodeFilter, Video,
    Weather, WeatherImage)
