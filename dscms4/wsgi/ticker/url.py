"""Ticker URL API."""

from wsgilib import JSON

from his import DATA, authenticated, authorized

from dscms4.messages.ticker import NoSuchTickerURL, TickerURLAdded, \
    TickerURLPatched, TickerURLDeleted
from dscms4.orm.ticker import URL
from dscms4.wsgi.ticker.ticker import get_ticker

__all__ = ['ROUTES']


def get_url(ticker, ident):
    """Returns the respective ticker URL."""

    try:
        return URL.get((URL.ticker == ticker) & (URL.id == ident))
    except URL.DoesNotExist:
        raise NoSuchTickerURL()


@authenticated
@authorized('dscms4')
def lst(ticker_id):
    """Lists all URLs of the respective ticker."""

    return JSON([url.to_dict() for url in URL.select().where(
        URL.ticker == get_ticker(ticker_id))])


@authenticated
@authorized('dscms4')
def get(ticker_id, url_id):
    """Returns the respective ticker URL."""

    return JSON(get_url(get_ticker(ticker_id), url_id).to_dict())


@authenticated
@authorized('dscms4')
def add(ticker_id):
    """Adds a new ticker URL."""

    ticker = get_ticker(ticker_id)
    url = URL.from_dict(ticker, DATA.json)
    url.save()
    return TickerURLAdded()


@authenticated
@authorized('dscms4')
def patch(ticker_id, url_id):
    """Patches a ticker URL."""

    ticker = get_ticker(ticker_id)
    url = get_url(ticker, url_id)
    url.patch(DATA.json)
    url.save()
    return TickerURLPatched()


@authenticated
@authorized('dscms4')
def delete(ticker_id, url_id):
    """Deletes a ticker URL."""

    ticker = get_ticker(ticker_id)
    url = get_url(ticker, url_id)
    url.delete_instance()
    return TickerURLDeleted()


ROUTES = (
    ('GET', '/ticker/<int:ticker_id>/url', lst, 'list_ticker_urls'),
    ('GET', '/ticker/<int:ticker_id>/url/<int:url_id>', get, 'get_ticker_url'),
    ('POST', '/ticker/<int:ticker_id>/url', add, 'add_ticker_url'),
    ('PATCH', '/ticker/<int:ticker_id>/url/<int:url_id>', patch,
     'patch_ticker_url'),
    ('DELETE', '/ticker/<int:ticker_id>/url/<int:url_id>', delete,
     'delete_ticker_url'))
