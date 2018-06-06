"""Configurations, colors, tickers and brightness settings."""

from contextlib import suppress
from datetime import datetime
from enum import Enum

from peewee import ForeignKeyField, TimeField, IntegerField, \
    SmallIntegerField, CharField, BooleanField, TextField

from peeweeplus import EnumField, CascadingFKField

from dscms4 import dom
from dscms4.orm.common import DSCMS4Model, CustomerModel

__all__ = [
    'Colors',
    'Configuration',
    'Ticker',
    'Text',
    'URL',
    'Backlight',
    'MODELS']


TIME_FORMAT = '%H:%M'


def percentage(value):
    """Restricts a number to 0-100 %."""

    value = round(value)

    if 0 <= value <= 100:
        return value

    raise ValueError('Invalid percentage: {}.'.format(value))


class Font(Enum):
    """Available fonts."""

    VERDANA = 'verdana'
    ARIAL = 'arial'
    LATO = 'lato'
    SPARKASSE = 'sparkasse'
    NETTOO = 'nettoo'


class Design(Enum):
    """Available designs."""

    THREE_D = '3d'
    NEWS = 'news'
    FLAT = 'flat'


class TickerTypes(Enum):
    """Valid ticker types."""

    TEXT = 'text'
    RSS = 'RSS'
    STOCK_PRICES = 'stock prices'


class Colors(DSCMS4Model):
    """Colors of a configuration."""

    header = IntegerField()
    header_background = IntegerField()
    background_left = IntegerField()
    background_right = IntegerField()
    ticker = IntegerField()
    ticker_background = IntegerField()
    clock = IntegerField()
    title = IntegerField()
    text = IntegerField()
    text_background = IntegerField()

    def to_dom(self):
        """Returns an XML DOM of the model."""
        xml = dom.Backlight()
        xml.header = self.header
        xml.header_background = self.header_background
        xml.background_left = self.background_left
        xml.background_right = self.background_right
        xml.ticker = self.ticker
        xml.ticker_background = self.ticker_background
        xml.clock = self.clock
        xml.title = self.title
        xml.text = self.text
        xml.text_background = self.text_background
        return xml


class Configuration(CustomerModel):
    """Customer configuration for charts."""

    name = CharField(255)
    description = CharField(255, null=True)
    font = EnumField(Font)
    portrait = BooleanField(default=False)
    touch = BooleanField()
    design = EnumField(Design)
    effects = BooleanField()
    ticker_speed = SmallIntegerField()
    colors = ForeignKeyField(Colors, column_name='colors')
    title_size = SmallIntegerField()
    text_size = SmallIntegerField()
    logo = IntegerField(null=True)
    background = IntegerField(null=True)
    dummy_picture = IntegerField(null=True)
    hide_cursor = BooleanField(default=True)
    rotation = SmallIntegerField(default=0)
    email_form = BooleanField()
    volume = SmallIntegerField()

    @classmethod
    def from_dict(cls, customer, dictionary, **kwargs):
        """Creates a new configuration from the provided
        dictionary for the respective customer.
        """
        colors = dictionary.pop('colors', {})
        tickers = dictionary.pop('tickers', ())
        backlights = dictionary.pop('backlight', {})
        configuration = super().from_dict(customer, dictionary, **kwargs)
        configuration.customer = customer
        colors = Colors.from_dict(colors)
        yield colors
        configuration.colors = colors
        yield configuration

        for ticker in tickers:
            yield from Ticker.from_dict(configuration, ticker)

        for backlight in Backlight.from_dict(
                backlights, configuration=configuration):
            yield backlight

    @property
    def backlight_dict(self):
        """Returns a backlight settings dictionary for this configuration."""
        backlights = {}

        for backlight in self.backlights:
            with suppress(ValueError):
                backlights.update(backlight.to_dict())

        return backlights

    def to_dict(self, **kwargs):
        """Converts the configuration into a JSON-like dictionary."""
        dictionary = super().to_dict(**kwargs)
        dictionary['colors'] = self.colors.to_dict()
        dictionary['tickers'] = [ticker.to_dict() for ticker in self.tickers]
        dictionary['backlight'] = self.backlight_dict
        return dictionary

    def patch(self, dictionary, **kwargs):
        """Patches the configuration."""
        colors = dictionary.pop('colors', None)
        tickers = dictionary.pop('tickers', None)
        backlights = dictionary.pop('backlight', None)
        yield super().patch(dictionary, **kwargs)

        if colors is not None:
            yield self.colors.patch(colors)

        if tickers is not None:
            for ticker in self.tickers:
                ticker.delete_instance()

            for ticker in tickers:
                yield from Ticker.from_dict(self, ticker)

        if backlights is not None:
            for backlight in self.backlights:
                backlight.delete_instance()

            for backlight in Backlight.from_dict(
                    backlights, configuration=self):
                yield backlight

    def to_dom(self):
        """Returns an XML DOM of the configuration."""
        xml = dom.Configuration()
        xml.name = self.name
        xml.description = self.description
        xml.font = self.font
        xml.portrait = self.portrait
        xml.touch = self.touch
        xml.design = self.design
        xml.effects = self.effects
        xml.ticker_speed = self.ticker_speed
        xml.colors = self.colors.to_dom()
        xml.title_size = self.title_size
        xml.text_size = self.text_size
        xml.logo = self.logo
        xml.background = self.background
        xml.dummy_picture = self.dummy_picture
        xml.hide_cursor = self.hide_cursor
        xml.rotation = self.rotation
        xml.email_form = self.email_form
        xml.volume = self.volume
        xml.ticker = [ticker.to_dom() for ticker in self.tickers]
        xml.backlight = [backlight.to_dom() for backlight in self.backlights]
        return xml

    def delete_instance(self):
        """Deletes this instance."""
        colors = self.colors
        result = super().delete_instance()
        colors.delete_instance()
        return result


class Ticker(DSCMS4Model):
    """Ticker."""

    configuration = CascadingFKField(
        Configuration, column_name='configuration', backref='tickers')
    type_ = EnumField(TickerTypes, column_name='type')

    @classmethod
    def from_dict(cls, configuration, dictionary):
        """Creates a new ticker from the respective dictionary."""
        texts = dictionary.pop('texts', ())
        urls = dictionary.pop('urls', ())
        ticker = super().from_dict(dictionary)
        ticker.configuration = configuration
        yield ticker

        for text in texts:
            yield Text.from_dict(ticker, text)

        for url in urls:
            yield URL.from_dict(ticker, url)

    def to_dict(self):
        """Returns a JSON-compliant dictionary."""
        dictionary = super().to_dict(primary_key=False)
        dictionary['texts'] = [text.to_dict() for text in self.texts]
        dictionary['urls'] = [url.to_dict() for url in self.urls]
        return dictionary

    def patch(self, dictionary):
        """Patches the ticker."""
        with suppress(KeyError):
            self.type_ = dictionary['type']

        yield self

        try:
            texts = dictionary['texts']
        except KeyError:
            pass
        else:
            texts = texts or ()

            for text in self.texts:
                text.delete_instance()

            for text in texts:
                yield Text.from_dict(self, text)

        try:
            urls = dictionary['urls']
        except KeyError:
            pass
        else:
            urls = urls or ()

            for url in self.urls:
                url.delete_instance()

            for url in urls:
                yield URL.from_dict(self, url)

    def to_dom(self):
        """Returns an XML DOM of the model."""
        xml = dom.Ticker()
        xml.type = self.type_
        xml.text = [text.to_dom() for text in self.texts]
        xml.url = [url.to_dom() for url in self.urls]
        return xml


class Text(DSCMS4Model):
    """Text for a ticker."""

    class Meta:
        table_name = 'ticker_text'

    ticker = ForeignKeyField(
        Ticker, column_name='ticker', backref='texts', on_delete='CASCADE')
    text = TextField()
    index = SmallIntegerField(default=0)

    @classmethod
    def from_dict(cls, ticker, dictionary):
        """Creates a ticker text from the given dictionary."""
        ticker_text = super().from_dict(dictionary)
        ticker_text.ticker = ticker
        return ticker_text

    def to_dict(self):
        """Returns a JSON-compliant dictionary."""
        return {'text': self.text, 'index': self.index}

    def to_dom(self):
        """Returns an XML DOM of the model."""
        return dom.Text(self.text, index=self.index)


class URL(DSCMS4Model):
    """Text for a ticker."""

    class Meta:
        table_name = 'ticker_url'

    ticker = ForeignKeyField(
        Ticker, column_name='ticker', backref='urls', on_delete='CASCADE')
    url = CharField(255)
    index = SmallIntegerField(default=0)

    @classmethod
    def from_dict(cls, ticker, dictionary):
        """Creates a ticker URL from the given dictionary."""
        ticker_url = super().from_dict(dictionary)
        ticker_url.ticker = ticker
        return ticker_url

    def to_dict(self):
        """Returns a JSON-compliant dictionary."""
        return {'url': self.url, 'index': self.index}

    def to_dom(self):
        """Returns an XML DOM of the model."""
        return dom.URL(self.text, index=self.index)


class Backlight(DSCMS4Model):
    """Backlight beightness settings of the respective configuration."""

    configuration = CascadingFKField(
        Configuration, column_name='configuration', backref='backlights')
    time = TimeField()
    brightness = SmallIntegerField()     # Brightness in percent.

    @classmethod
    def from_dict(cls, dictionary, configuration=None):
        """Yields new records from the provided dictionary."""
        for time, brightness in dictionary.items():
            time = datetime.strptime(time, TIME_FORMAT).time()
            record = super().from_dict(
                {'time': time, 'brightness': brightness})
            record.configuration = configuration
            yield record

    @property
    def percent(self):
        """Returns the percentage as an integer."""
        return percentage(self.brightness)

    @percent.setter
    def percent(self, brightness):
        """Sets the percentage."""
        self.brightness = percentage(brightness)

    def to_dict(self):
        """Returns the backlight as dictionary."""
        return {self.time.strftime(TIME_FORMAT): self.percent}

    def to_dom(self):
        """Returns an XML DOM of the model."""
        xml = dom.Backlight()
        xml.time = self.time
        xml.brightness = self.brightness
        return xml


MODELS = (Colors, Configuration, Ticker, Text, URL, Backlight)
