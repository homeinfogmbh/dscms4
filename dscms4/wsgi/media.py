"""User's media files."""

from his import CUSTOMER
from wsgilib import routed, JSON

from dscms4.orm.media import MediaFile

__all__ = ['ROUTES']


def _get_media_files():
    """Yields the current customer's media files."""

    return MediaFile.select().where(MediaFile.customer == CUSTOMER.id)


MEDIA_FILES = LocalProxy(_get_media_files)


def _get_media_file(ident):
    """Returns the respective media file for the current customer."""

    try:
        return MediaFile.get(
            (MediaFile.customer == CUSTOMER.id) & (MediaFile.id == ident))
    except DoesNotExist:
        raise NoSuchMediaFile()


def lst():
    """Lists the media files of the current customer."""

    return JSON([media_file.to_dict() for media_file in MEDIA_FILES])


def get(ident):
    """Returns the respective media file."""

    return JSON(_get_media_file(ident).to_dict())


ROUTES = (
    ('GET', '/media', get, 'list_media'),
    ('GET', '/media/<int:ident>', get, 'get_media')
