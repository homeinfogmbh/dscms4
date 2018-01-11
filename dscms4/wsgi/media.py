"""User's media files."""

from flask import request
from peewee import DoesNotExist
from werkzeug.local import LocalProxy

from his import CUSTOMER, DATA
from wsgilib import JSON, Binary

from dscms4.messages.media import NoSuchMediaFile, QuotaExceeded, \
    MediaFileAdded
from dscms4.orm.exceptions import QuotaExceeded as QuotaExceeded_
from dscms4.orm.media import MediaSettings, MediaFile

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

    media_file = _get_media_file(ident)

    try:
        request.args['metadata']
    except KeyError:
        return JSON(media_file.to_dict())

    return Binary(media_file.data)


def post():
    """Returns the respective media file."""

    try:
        media_file = MediaFile.from_bytes(DATA.bytes, customer=CUSTOMER.id)
    except QuotaExceeded_:
        raise QuotaExceeded()

    media_file.save()
    return MediaFileAdded(id=media_file.id)


def delete(ident):
    """Deletes the respective media file."""

    _get_media_file(ident).delete_instance()
    return MediaFileDeleted()


def get_settings():
    """Returns the respective media settings."""

    return JSON(MediaSettings.get(
        MediaSettings.customer == CUSTOMER.id).to_dict())


ROUTES = (
    ('GET', '/media/file', lst, 'list_media_files'),
    ('GET', '/media/file/<int:ident>', get, 'get_media_file'),
    ('POST', '/media/file', post, 'post_media_file'),
    ('DELETE', '/media/file/<int:ident>', delete, 'delete_media_file'),
    ('GET', '/media/settings', post, 'get_media_settings'))
