"""Media file manager."""

from contextlib import suppress
from hashlib import sha256

from filedb import File, FileProperty
from peewee import DoesNotExist, IntegerField

from .common import DSCMS4Model, CustomerModel
from .exceptions import QuotaExceeded

__all__ = ['MediaSettings', 'MediaFile']


BINARY_FACTOR = 1024
BYTE = 1
KIBIBYTE = BYTE * BINARY_FACTOR
MEBIBYTE = KIBIBYTE * BINARY_FACTOR
GIBIBATE = MEBIBYTE * BINARY_FACTOR

DEFAULT_QUOTA = 5 * GIBIBATE    # 5.0 GiB.

PARAMETER_ERROR = TypeError('Must specify either file ID or bytes.')


def check_quota(customer, bytes_):
    """Checks whether customer quota suffices
    for storing the respective bytes.
    """

    media_settings = MediaSettings.by_customer(customer)

    if media_settings.free >= len(bytes_):
        return True

    raise QuotaExceeded(media_settings.quota)


class MediaSettings(DSCMS4Model, CustomerModel):
    """Media settings for a customer."""

    quota = IntegerField(default=DEFAULT_QUOTA)     # Customer quota in bytes.

    @classmethod
    def by_customer(cls, customer):
        """Returns the settings for the respective customer."""
        return cls.get(cls.customer == customer)

    @property
    def media_files(self):
        """Yields media file records of the respective customer."""
        return MediaFile.select().where(MediaFile.customer == self.customer)

    @property
    def files(self):
        """Yields instances of filedb.File the customer uses."""
        for media_file in self.media_files:
            yield media_file.file

    @property
    def used(self):
        """Returns used space."""
        return sum(file.size for file in self.files)

    @property
    def free(self):
        """Returns free space for the respective customer."""
        return self.quota - self.used

    def to_dict(self):
        """Returns a JSON compliant dictionary."""
        dictionary = super().to_dict()
        dictionary.update({
            'quota': self.quota,
            'free': self.free,
            'used': self.used})
        return dictionary


class MediaFile(DSCMS4Model, CustomerModel):
    """A media file of the respective customer."""

    file = IntegerField()
    data = FileProperty(file)

    @classmethod
    def from_bytes(cls, data, customer=None, ignore_quota=False):
        """Adds a new media file by bytes."""
        with suppress(DoesNotExist):
            return cls.by_sha256sum(sha256(data).hexdigest())

        if ignore_quota or check_quota(customer, data):
            record = cls()
            record.data = data
            record.customer = customer
            return record

    @classmethod
    def by_sha256sum(cls, sha256sum):
        """Returns the respective media file by
        its's corresponding SHA-256 checksum.
        """
        return cls.get(cls.file == File.get(File.sha256sum == sha256sum).id)

    def to_dict(self):
        """Returns a JSON compliant dictionary of the file's meta data."""
        dictionary = super().to_dict()
        file = self.data
        dictionary.update({
            'mimetype': file.mimetype,
            'sha256sum': file.sha256sum,
            'size': file.size})
        return dictionary

    def delete_instance(self, *args, **kwargs):
        """Deletes the respective file."""
        self.data.unlink()
        return super().delete_instance(*args, **kwargs)
