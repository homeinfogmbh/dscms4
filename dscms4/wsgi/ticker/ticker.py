"""WSGI controllers for tickers."""

from his import CUSTOMER, DATA, authenticated, authorized

from wsgilib import JSON

from dscms4.messages.ticker import NoSuchTicker, TickerAdded, TickerPatched, \
    TickerDeleted
from dscms4.orm.configuration import Ticker

__all__ = ['get_ticker', 'ROUTES']


def get_tickers():
    """Yields tickers of the current user."""

    return Ticker.select().where(Ticker.customer == CUSTOMER.id)


def get_ticker(ident):
    """Returns the respective ticker of the customer."""

    try:
        return Ticker.get(
            (Ticker.id == ident) & (Ticker.customer == CUSTOMER.id))
    except Ticker.DoesNotExist:
        raise NoSuchTicker()


@authenticated
@authorized('dscms4')
def lst():
    """Lists tickers of the respective customer."""

    return JSON([ticker.to_dict() for ticker in get_tickers()])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective ticker."""

    return JSON(get_ticker(ident).to_dict())


@authenticated
@authorized('dscms4')
def add():
    """Adds a new ticker."""

    try:
        ticker = Ticker.from_dict(DATA.json)
        ident = ticker.save()
    except ValueError:
        pass

    return TickerAdded(id=ident)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Adds a new ticker."""

    ticker = get_ticker(ident)

    try:
        ticker.patch(DATA.json)
    except ValueError:
        pass

    return TickerPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Adds a new ticker."""

    get_ticker(ident).delete_instance()
    return TickerDeleted()


ROUTES = (
    ('GET', '/ticker', lst, 'list_tickers'),
    ('GET', '/ticker/<int:ident>', get, 'get_ticker'),
    ('POST', '/ticker', add, 'add_ticker'),
    ('PATCH', '/ticker/<int:ident>', patch, 'patch_ticker'),
    ('DELETE', '/ticker/<int:ident>', delete, 'delete_ticker'))
