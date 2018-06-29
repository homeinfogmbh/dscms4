"""File hooks."""

from dscms4.orm.charts.image_text import Image as ITCImage
from dscms4.orm.charts.video import Video
from dscms4.orm.charts.weather import Image as WCImage
from dscms4.orm.configuration import Configuration

__all__ = ['on_delete']


def _remove_itc_images(ident):
    """Removes the respective Images of ImageTest charts."""

    ITCImage.delete().where(ITCImage.image == ident)


def _remove_wc_image(ident):
    """Removes the respective Images of Weather charts."""

    WCImage.delete().where(WCImage.image == ident)


def _remove_video_charts(ident):
    """Removes the respective video charts."""

    for video in Video.select().where(Video.video == ident):
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
            configuration.logo = None

        if configuration.background == ident:
            configuration.background = None

        if configuration.dummy_picture == ident:
            configuration.dummy_picture = None

        configuration.save()


def on_delete(ident):
    """Runs when the file with the respective ID has been deleted."""

    _remove_itc_images(ident)
    _remove_wc_image(ident)
    _remove_video_charts(ident)
    _null_configurations(ident)
