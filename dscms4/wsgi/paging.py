"""Paging."""

from math import ceil

from flask import request

from his.messages import MissingData, InvalidData

__all__ = ['page']


def _count_pages(iterable, size):
    """Counts the pages."""

    items = 0

    for items, _ in enumerate(iterable, start=1):
        pass

    return {'pages': ceil(items / size)}


def _page(iterable, size, pageno):
    """Pages the respective iterable."""

    offset = size * pageno
    end = offset + size

    for index, item in enumerate(iterable):
        if index == end:
            break
        elif offset <= index:
            yield item


def page(iterable):
    """Returns the respective page or page count."""

    try:
        size = int(request.args['size'])
    except KeyError:
        raise MissingData(parameter='size')
    except ValueError:
        raise InvalidData(parameter='size')

    try:
        pageno = int(request.args['page'])
    except KeyError:
        return _count_pages(iterable, size)
    except ValueError:
        raise InvalidData(parameter='page')

    return _page(iterable, size, pageno)
