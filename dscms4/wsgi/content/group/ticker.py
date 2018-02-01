"""Management of tickers in groups."""

from wsgilib import JSON

from dscms4.messages.content.group import NoSuchGroupTicker, \
    TickerAddedToGroup, TickerAlreadyInGroup, TickerDeletedFromGroup
from dscms4.orm.content.group import GroupTicker
from dscms4.wsgi.group import _get_group
from dscms4.wsgi.ticker import _get_ticker

__all__ = ['ROUTES']


def get(gid):
    """Returns a list of IDs of the menus in the respective group."""

    return JSON([
        group_ticker.ticker.id for group_ticker in GroupTicker.select().where(
            GroupTicker.group == _get_group(gid))])


def add(gid, ident):
    """Adds the menu to the respective group."""

    group = _get_group(gid)
    ticker = _get_ticker(ident)

    try:
        GroupTicker.get(
            (GroupTicker.group == group) & (GroupTicker.ticker == ticker))
    except GroupTicker.DoesNotExist:
        group_ticker = GroupTicker()
        group_ticker.group = group
        group_ticker.ticker = ticker
        group_ticker.save()
        return TickerAddedToGroup()

    return TickerAlreadyInGroup()


def delete(gid, ident):
    """Deletes the menu from the respective group."""

    try:
        group_ticker = GroupTicker.get(
            (GroupTicker.group == _get_group(gid)) & (GroupTicker.id == ident))
    except GroupTicker.DoesNotExist:
        raise NoSuchGroupTicker()

    group_ticker.delete_instance()
    return TickerDeletedFromGroup()


ROUTES = (
    ('GET', '/content/group/<int:gid>/ticker', get, 'list_group_ticker'),
    ('POST', '/content/group/<int:gid>/ticker', add, 'add_group_ticker'),
    ('DELETE', '/content/group/<int:gid>/ticker/<int:ident>', delete,
     'delete_group_ticker'))
