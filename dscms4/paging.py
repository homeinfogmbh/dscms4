"""Paging."""

__all__ = ['page', 'pages']


def page(iterable, size, pageno):
    """Pages the respective iterable."""

    offset = size * pageno
    end = offset + size

    for index, item in enumerate(iterable):
        if index == end:
            break
        elif offset <= index:
            yield item


def pages(iterable, size):
    """Counts the pages."""

    items = 0

    for items, _ in enumerate(iterable, start=1):
        pass

    pages_ = items // size

    if items % size:
        return pages_ + 1

    return pages_
