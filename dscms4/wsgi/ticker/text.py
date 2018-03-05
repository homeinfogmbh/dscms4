"""Ticker text API."""

from his import DATA

from wsgilib import JSON

from his import authenticated, authorized

from dscms4.messages.ticker import NoSuchTickerText, TickerTextAdded, \
    TickerTextPatched, TickerTextDeleted
from dscms4.orm.configuration import Text
from dscms4.wsgi.ticker.ticker import get_ticker

__all__ = ['ROUTES']


def get_text(ticker, ident):
    """Returns the respective ticker text."""

    try:
        return Text.get((Text.ticker == ticker) & (Text.id == ident))
    except Text.DoesNotExist:
        raise NoSuchTickerText()


@authenticated
@authorized('dscms4')
def list_(ticker_id):
    """Lists all texts of the respective ticker."""

    return JSON([text.to_dict() for text in Text.select().where(
        Text.ticker == get_ticker(ticker_id))])


@authenticated
@authorized('dscms4')
def get(ticker_id, text_id):
    """Returns the respective ticker text."""

    return JSON(get_text(get_ticker(ticker_id), text_id).to_dict())


@authenticated
@authorized('dscms4')
def add(ticker_id):
    """Adds a new ticker text."""

    ticker = get_ticker(ticker_id)
    text = Text.from_dict(ticker, DATA.json)
    text.save()
    return TickerTextAdded()


@authenticated
@authorized('dscms4')
def patch(ticker_id, text_id):
    """Patches a ticker text."""

    ticker = get_ticker(ticker_id)
    text = get_text(ticker, text_id)
    text.patch(DATA.json)
    text.save()
    return TickerTextPatched()


@authenticated
@authorized('dscms4')
def delete(ticker_id, text_id):
    """Deletes a ticker text."""

    ticker = get_ticker(ticker_id)
    text = get_text(ticker, text_id)
    text.delete_instance()
    return TickerTextDeleted()


ROUTES = (
    ('GET', '/ticker/<int:ticker_id>/text', list_, 'list_ticker_texts'),
    ('GET', '/ticker/<int:ticker_id>/text/<int:text_id>', get,
     'get_ticker_text'),
    ('POST', '/ticker/<int:ticker_id>/text', add, 'add_ticker_text'),
    ('PATCH', '/ticker/<int:ticker_id>/text/<int:text_id>', patch,
     'patch_ticker_text'),
    ('DELETE', '/ticker/<int:ticker_id>/text/<int:text_id>', delete,
     'delete_ticker_text'))
