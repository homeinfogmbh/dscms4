"""Tickers."""

from sys import stderr
from contextlib import suppress

from peewee import Model, ForeignKeyField, SmallIntegerField, CharField, \
    TextField
from homeinfo.crm import Customer

from .common import DSCMS4Model, CustomerModel

__all__ = [
    'Ticker',
    'TickerText',
    'TickerURL',
    'TickerTextMapping',
    'TickerURLMapping']


def create_tables():
    """Creates database tables."""

    for model in MODELS:
        try:
            model.create_table()
        except Exception:
            print('Could not create table for {}.'.format(model), file=stderr)


class Ticker(Model, CustomerModel):
    """Ticker."""

    customer = ForeignKeyField(Customer, db_column='customer')
    name = CharField(255)

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a new ticker from the respective dictionary."""
        ticker = cls()
        ticker.customer = customer
        ticker.name = dictionary['name']
        ticker.save()
        return ticker

    def to_dict(self, recursive=False):
        """Returns a JSON-compliant dictionary."""
        dictionary = {'name': self.name}

        if recursive:
            dictionary['texts'] = [
                ticker_text.text.to_dict() for
                ticker_text in self.texts]
            dictionary['urls'] = [
                ticker_url.url.to_dict() for
                ticker_url in self.urls]

        return dictionary

    def patch(self, dictionary):
        """Patches the ticker with the given dictionary."""
        with suppress(KeyError):
            self.name = dictionary['name']

        self.save()


class TickerText(Model, CustomerModel):
    """Text for a ticker."""

    class Meta:
        db_table = 'ticker_text'

    customer = ForeignKeyField(Customer, db_column='customer')
    text = TextField()
    index = SmallIntegerField()

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a ticker text from the given dictionary."""
        ticker_text = cls()
        ticker_text.customer = customer
        ticker_text.text = dictionary['text']
        ticker_text.index = dictionary.get('index', 0)
        ticker_text.save()
        return ticker_text

    def to_dict(self):
        """Returns a JSON-compliant dictionary."""
        return {
            'text': self.text,
            'index': self.index}

    def patch(self, dictionary):
        """Patches the ticker text with the given dictionary."""
        with suppress(KeyError):
            self.text = dictionary['text']

        with suppress(KeyError):
            self.index = dictionary['index']

        self.save()


class TickerURL(Model, CustomerModel):
    """Text for a ticker."""

    class Meta:
        db_table = 'ticker_url'

    customer = ForeignKeyField(Customer, db_column='customer')
    url = CharField(255)
    index = SmallIntegerField()

    @classmethod
    def from_dict(cls, customer, dictionary):
        """Creates a ticker URL from the given dictionary."""
        ticker_url = cls()
        ticker_url.customer = customer
        ticker_url.url = dictionary['url']
        ticker_url.index = dictionary.get('index', 0)
        ticker_url.save()
        return ticker_url

    def to_dict(self):
        """Returns a JSON-compliant dictionary."""
        return {
            'url': self.url,
            'index': self.index}

    def patch(self, dictionary):
        """Patches the ticker text with the given dictionary."""
        with suppress(KeyError):
            self.url = dictionary['url']

        with suppress(KeyError):
            self.index = dictionary['index']

        self.save()


class TickerTextMapping(Model, DSCMS4Model):
    """Ticker-text mapping."""

    class Meta:
        db_table = 'ticker_texts'

    ticker = ForeignKeyField(Ticker, db_column='ticker', related_name='texts')
    text = ForeignKeyField(
        TickerText, db_column='text', related_name='tickers')


class TickerURLMapping(Model, DSCMS4Model):
    """Ticker-URL mapping."""

    class Meta:
        db_table = 'ticker_urls'

    ticker = ForeignKeyField(Ticker, db_column='ticker', related_name='urls')
    url = ForeignKeyField(TickerURL, db_column='url', related_name='tickers')


MODELS = (Ticker, TickerText, TickerURL, TickerTextMapping, TickerURLMapping)
