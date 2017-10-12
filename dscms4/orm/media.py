"""Media file manager."""

from contextlib import suppress
from hashlib import sha256

from filedb import File, FileClient, FileProperty
from peewee import DoesNotExist, Model, IntegerField

from .common import CustomerModel
from .exceptions import QuotaExceeded

__all__ = ['MediaSettings', 'MediaFile']


BINARY_FACTOR = 1024
KIBIBYTE = BINARY_FACTOR
MEBIBYTE = BINARY_FACTOR * KIBIBYTE
GIBIBATE = BINARY_FACTOR * MEBIBYTE

DEFAULT_QUOTA = 5 * GIBIBATE    # 5.0 GiB.

FILE_CLIENT = FileClient('5bb119d7-5cd8-499c-a485-2e93a6333e12')
PARAMETER_ERROR = TypeError('Must specify either file_id or bytes.')


def check_quota(customer, bytes_):
    """Checks whether customer quota suffices
    for storing the respective bytes.
    """

    media_settings = MediaSettings.by_customer(customer)

    if media_settings.free >= len(bytes_):
        return True

    raise QuotaExceeded(media_settings.quota)


class MediaSettings(Model, CustomerModel):
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


class MediaFile(Model, CustomerModel):
    """A media file of the respective customer."""

    file_id = IntegerField()
    file = FileProperty(file_id, file_client=FILE_CLIENT)

    @classmethod
    def add(cls, customer, bytes_, ignore_quota=False):
        """Adds a new media file by bytes."""
        with suppress(DoesNotExist):
            file = File.get(File.sha256sum == sha256(bytes_).hexdigest())
            return cls.get(cls.file == file)

        if ignore_quota or check_quota(customer, bytes_):
            record = cls()
            record.customer = customer
            record.file = bytes_
            record.save()
            return record

    def to_dict(self):
        """Returns a JSON compliant dictionary of the file's meta data."""
        dictionary = super().to_dict()
        file = self.file
        dictionary.update({
            'mimetype': file.mimetype,
            'sha256sum': file.sha256sum,
            'size': file.size})
        return dictionary
