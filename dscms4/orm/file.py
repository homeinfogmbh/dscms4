"""Customer-related data."""

from uuid import uuid4

from filedb import FileError, add, get, delete, sha256sum, mimetype, size, \
    File as File_
from peewee import ForeignKeyField, CharField

from dscms4.orm.common import CustomerModel


class FileExists(Exception):
    """Indicates that a file with the respective name already exists."""

    pass


class File(CustomerModel):
    """Represents files associated with a customer."""

    file = ForeignKeyField(File_, column_name='file')
    name = CharField(255)

    @classmethod
    def add(cls, customer, data, name=None):
        """Adds a file."""
        if not name:
            name = str(uuid4())

        try:
            cls.get((cls.customer == customer) & (cls.name == name))
        except cls.DoesNotExist:
            file = cls()
            file.customer = customer
            file.file = add(data)
            file.name = name
            return file

        raise FileExists()

    @property
    def data(self):
        """Returns the actual file data."""
        return get(self.file)

    def to_dict(self):
        """Returns a JSON-ish dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'sha256sum': sha256sum(self.file),
            'mimetype': mimetype(self.file),
            'size': size(self.file)}

    def delete_instance(self, recursive=False, delete_nullable=False):
        """Removes the respective file."""
        try:
            delete(self.file)
        except FileError:
            file_del = False
        else:
            file_del = True

        return super().delete_instance(
            recursive=recursive, delete_nullable=delete_nullable) and file_del
