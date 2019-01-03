"""Hooks for filedb actions."""

from logging import INFO, basicConfig, getLogger

from dscms4.config import LOG_FORMAT
from dscms4.orm.charts.blackboard import Image as BlackboardChartImage
from dscms4.orm.charts.image_text import Image as ImageTextChartImage
from dscms4.orm.charts.video import Video
from dscms4.orm.charts.weather import Image as WeatherChartImage
from dscms4.orm.configuration import Configuration


__all__ = ['on_delete']


LOGGER = getLogger('dscms4.file_hooks')
basicConfig(level=INFO, format=LOG_FORMAT)


def _remove_bc_images(ident):
    """Removes the respective images of Blackboard charts."""

    for image in BlackboardChartImage.select().where(
            BlackboardChartImage.image == ident):
        LOGGER.info(
            'Deleting blackboard.Image %i with image %i.',
            image.id, ident)
        image.delete_instance()


def _remove_itc_images(ident):
    """Removes the respective images of ImageText charts."""

    for image in ImageTextChartImage.select().where(
            ImageTextChartImage.image == ident):
        LOGGER.info(
            'Deleting image_text.Image %i with image %i.',
            image.id, ident)
        image.delete_instance()


def _remove_wc_image(ident):
    """Removes the respective images of Weather charts."""

    for image in WeatherChartImage.select().where(
            WeatherChartImage.image == ident):
        LOGGER.info(
            'Deleting weather.Image %i with image %i.',
            image.id, ident)
        image.delete_instance()


def _null_video_charts(ident):
    """Sets the image fields of the
    respective video charts to NULL.
    """

    for video in Video.select().where(Video.video == ident):
        LOGGER.info('Setting video = %i to NULL on Video %i.', ident, video.id)
        video.video = None
        video.save()


def _null_configurations(ident):
    """Sets the image fields of the
    respective configurations to NULL.
    """

    for configuration in Configuration.select().where(
            (Configuration.logo == ident)
            | (Configuration.background == ident)
            | (Configuration.dummy_picture == ident)):
        if configuration.logo == ident:
            LOGGER.info(
                'Setting logo = %i to NULL on Configuration %i.',
                ident, configuration.id)
            configuration.logo = None

        if configuration.background == ident:
            LOGGER.info(
                'Setting background = %i to NULL on Configuration %i.',
                ident, configuration.id)
            configuration.background = None

        if configuration.dummy_picture == ident:
            LOGGER.info(
                'Setting dummy_picture = %i to NULL on Configuration %i.',
                ident, configuration.id)
            configuration.dummy_picture = None

        configuration.save()


def on_delete(ident):
    """Runs when the file with the respective ID has been deleted."""

    _remove_bc_images(ident)
    _remove_itc_images(ident)
    _remove_wc_image(ident)
    _null_video_charts(ident)
    _null_configurations(ident)
