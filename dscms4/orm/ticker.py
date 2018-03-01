"""Tickers."""

from contextlib import suppress

from peewee import ForeignKeyField, SmallIntegerField, CharField, TextField

from peeweeplus import CascadingFKField

from dscms4.orm.common import DSCMS4Model
from dscms4.orm.configuration import Configuration

__all__ = ['Ticker', 'Text', 'URL', 'MODELS']


class Ticker(DSCMS4Model):
    """Ticker."""

    configuration = CascadingFKField(
        Configuration, column_name='configuration')
    name = CharField(255)

    @classmethod
    def from_dict(cls, configuration, dictionary):
        """Creates a new ticker from the respective dictionary."""
        name = dictionary.pop('name')
        ticker = super().from_dict(dictionary)
        ticker.configuration = configuration
        ticker.name = name
        ticker.save()
        return ticker

    @property
    def texts(self):
        """Yields the ticker's texts."""
        return Text.select().where(Text.ticker == self)

    @property
    def urls(self):
        """Yields the ticker's URLs."""
        return URL.select().where(URL.ticker == self)

    def to_dict(self, recursive=False):
        """Returns a JSON-compliant dictionary."""
        dictionary = {'name': self.name}

        if recursive:
            dictionary['texts'] = [
                ticker_text.text.to_dict() for ticker_text in self.texts]
            dictionary['urls'] = [
                ticker_url.url.to_dict() for ticker_url in self.urls]

        return dictionary

    def patch(self, dictionary):
        """Patches the ticker with the given dictionary."""
        with suppress(KeyError):
            self.name = dictionary['name']

        self.save()


class Text(DSCMS4Model):
    """Text for a ticker."""

    class Meta:
        table_name = 'ticker_text'

    ticker = ForeignKeyField(Ticker, column_name='ticker', on_delete='CASCADE')
    text = TextField()
    index = SmallIntegerField()

    @classmethod
    def from_dict(cls, ticker, dictionary):
        """Creates a ticker text from the given dictionary."""
        ticker_text = cls()
        ticker_text.ticker = ticker
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


class URL(DSCMS4Model):
    """Text for a ticker."""

    class Meta:
        table_name = 'ticker_url'

    ticker = ForeignKeyField(Ticker, column_name='ticker', on_delete='CASCADE')
    url = CharField(255)
    index = SmallIntegerField()

    @classmethod
    def from_dict(cls, ticker, dictionary):
        """Creates a ticker URL from the given dictionary."""
        ticker_url = cls()
        ticker_url.ticker = ticker
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


MODELS = (Ticker, Text, URL)
