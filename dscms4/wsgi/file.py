"""DSCMS4 WSGI handlers for files."""

from flask import request

from his import CUSTOMER, authenticated, authorized
from wsgilib import Binary, JSON

from dscms4.messages.file import NoSuchFile, FilesAdded, FileExists, \
    FileDeleted
from dscms4.orm.file import FileExists as FileExists_, File

__all__ = ['ROUTES']


def get_files():
    """Yields the respective files."""

    return File.select().where(File.customer == CUSTOMER.id)


def get_file(ident):
    """Returns the respective file."""

    try:
        return File.get((File.customer == CUSTOMER.id) & (File.id == ident))
    except File.DoesNotExist:
        raise NoSuchFile()


def add_file(data, name):
    """Adds the respective file."""

    try:
        file = File.add(CUSTOMER.id, data, name=name)
    except FileExists_:
        raise FileExists(name=name)

    file.save()
    return file


@authenticated
@authorized('dscms4')
def list_():
    """Lists IDs of charts of the respective customer."""

    return JSON([file.to_dict() for file in get_files()])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective chart of the current customer."""

    file = get_file(ident)

    if request.args.get('metadata', False):
        return JSON(file.to_dict())

    filename = file.name if request.args.get('named', False) else None
    return Binary(file.data, filename=filename)


@authenticated
@authorized('dscms4')
def add():
    """Adds new charts."""

    files = []

    for name, file_storage in request.files.items():
        data = file_storage.stream.read()
        file = add_file(data, name)
        files.append({file.id: file.name})

    return FilesAdded(files=files)


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes the specified chart."""

    get_file(ident).delete_instance()
    return FileDeleted()


ROUTES = (
    ('GET', '/file', list_, 'list_files'),
    ('GET', '/file/<int:ident>', get, 'get_files'),
    ('POST', '/file', add, 'add_files'),
    ('DELETE', '/file/<int:ident>', delete, 'delete_file'))
