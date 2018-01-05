"""User's media files."""

from wsgilib import routed, JSON

from dscms4.orm.media import MediaFile
from dscms4.wsgi.common import DSCMS4Service


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


@routed('/media/[id:int]')
class MediaHandler(DSCMS4Service):
    """Handles user's media files."""

    @property

    @property
    def file(self):
        """Returns the selected file."""
        return MediaFile.get(
            (MediaFile.id == self.vars['id'])
            & (MediaFile.customer == self.customer))

    def list(self):
        """Lists available media files."""
        return JSON([file.to_dict() for file in self.files])

    def get(self):
        """Returns media files."""
        if self.vars['id'] is None:
            return self.list()

        return JSON(self.file.to_dict())
