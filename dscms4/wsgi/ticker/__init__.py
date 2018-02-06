"""WSGI controllers for tickers, texts and URLs."""

from dscms4.wsgi.ticker import ticker, text, url
from dscms4.wsgi.ticker.ticker import get_ticker

__all__ = ['get_ticker', 'ROUTES']


ROUTES = ticker.ROUTES + text.ROUTES + url.ROUTES
