"""Ticker text API."""

from wsgilib import JSON

from his import authenticated, authorized

from dscms4.orm.ticker import Text
from dscms4.wsgi.ticker.ticker import get_ticker


def get_text(ticker, ident):
    """Returns the respective ticker text."""

    try:
        return Text.get((Text.ticker == ticker) & (Text.id == ident))
    except Text.DoesNotExist:
        raise NoSuchTickerText()


@authenticated
@authorized('dscms4')
def lst(ticker_id):
    """Lists all texts of the respective ticker."""

    return JSON([text.to_dict() for text in Text.select().where(
        Text.ticker == get_ticker(ticker_id))])


@authenticated
@authorized('dscms4')
def get(ticker_id, text_id):
    """Returns the respective ticker text."""

    return JSON(get_text(get_ticker(ticker_id), text_id).to_dict())
