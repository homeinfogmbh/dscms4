"""WSGI controllers for tickers."""

from wsgilib import JSON

from dscms4.orm.ticker import Ticker

__all__ = ['ROUTES']


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


ROUTES = (
    ('GET', '/ticker', lst, 'list_tickers'),
    ('GET', '/ticker/<int:ident>', get, 'get_ticker'))
