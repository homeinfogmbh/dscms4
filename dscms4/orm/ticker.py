"""Tickers"""

from peewee import ForeignKeyField, SmallIntegerField, CharField, TextField

from .common import DSCMS4Model

__all__ = [
    'Ticker',
    'TickerText',
    'TickerURL']


class Ticker(DSCMS4Model):
    """Ticker"""

    name = CharField(255)


class TickerText(DSCMS4Model):
    """Text for a ticker"""

    class Meta:
        db_table = 'ticker_text'

    ticker = ForeignKeyField(Ticker, db_column='ticker')
    text = TextField()
    index = SmallIntegerField()


class TickerURL(DSCMS4Model):
    """Text for a ticker"""

    class Meta:
        db_table = 'ticker_url'

    ticker = ForeignKeyField(Ticker, db_column='ticker')
    url = CharField(255)
    index = SmallIntegerField()
