"""WSGI controllers for tickers, texts and URLs."""

from dscms4.wsgi.ticker import ticker, text, url

__all__ = ['ROUTES']


ROUTES = ticker.ROUTES + text.ROUTES + url.ROUTES
