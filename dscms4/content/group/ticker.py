"""Group ticker content."""

from dscms4.content.common import ContentInformation
from dscms4.orm.content.group import GroupTicker

__all__ = ['tickers', 'accumulated_tickers']


def tickers(group):
    """Yields tickers of this group."""

    for group_ticker in GroupTicker.select().where(GroupTicker.group == group):
        yield ContentInformation(group, group_ticker.ticker)


def accumulated_tickers(group):
    """Yields accumulated tickers of this group."""

    yield from tickers(group)
    parent = group.parent

    if parent:
        yield from accumulated_tickers(parent)
