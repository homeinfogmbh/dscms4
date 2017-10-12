"""Media file manager."""

from peewee import Model, IntegerField

from filedb import FileClient, FileProperty

from .common import CustomerModel
from .exceptions import QuotaExceeded


BINARY_FACTOR = 1024
KIBIBYTE = BINARY_FACTOR
MEBIBYTE = BINARY_FACTOR * KIBIBYTE
GIBIBATE = BINARY_FACTOR * MEBIBYTE

DEFAULT_QUOTA = 5 * GIBIBATE    # 5.0 GiB.

FILE_CLIENT = FileClient('5bb119d7-5cd8-499c-a485-2e93a6333e12')
PARAMETER_ERROR = TypeError('Must specify either file_id or bytes.')


def check_free(free, obj):
    """Checks whether free space suffices for storing the provided object.

    :free: Free space in bytes.
    :obj: int for file ID or bytes.
    """

    if isinstance(obj, bytes):
        return free >= len(bytes)
    elif isinstance(obj, int):
        file = FILE_CLIENT.get(obj)
        return free >= file.size

    raise TypeError('Unsupported type: {} ({}).'.format(obj, type(obj)))


def check_quota(customer, obj):
    """Checks whether customer quota suffices for the respective object.

    :customer: The respective customer.
    :obj: int for file ID or bytes.
    """

    media_settings = MediaSettings.by_customer(customer)

    if check_free(media_settings.free, obj):
        return True

    raise QuotaExceeded(media_settings.quota)


class MediaSettings(Model, CustomerModel):
    """Media settings for a customer."""

    quota = IntegerField(default=DEFAULT_QUOTA)

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
        """Yields files the customer uses."""
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
    def add_file(cls, customer, file_id, force=False):
        """Adds a file."""
        if force or check_quota(customer, file_id):
            record = cls()
            record.file_id = file_id
            record.save()
            return record

    @classmethod
    def add_bytes(cls, customer, bytes, force=False):
        """Adds bytes."""
        if force or check_quota(customer, bytes):
            record = cls()
            record.file = bytes
            record.save()
            return record

        raise QuotaExceeded()

    @classmethod
    def add(cls, customer, *, file_id=None, bytes=None, force=False):
        """Adds file ID or bytes."""
        if file_id is not None and bytes is not None:
            raise PARAMETER_ERROR
        elif file_id is not None:
            return cls.add_file(customer, file_id, force=force)
        elif bytes is not None:
            return cls.add_bytes(customer, bytes, force=force)
        else:
            raise PARAMETER_ERROR
