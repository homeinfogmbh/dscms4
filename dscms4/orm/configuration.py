"""Configurations, colors, tickers and brightness settings."""

from enum import Enum

from peewee import ForeignKeyField, TimeField, IntegerField, \
    SmallIntegerField, CharField, BooleanField, TextField

from peeweeplus import EnumField

from .common import DSCMS4Model, CustomerModel

__all__ = [
    'Colors',
    'Configuration',
    'Backlight',
    'MODELS']


def percentage(value):
    """Returns the percentage of a decimal number."""

    value = round(value)

    if 0 <= value <= 100:
        return value

    raise ValueError('Invalid percentage: {}.'.format(value))


def stripped_time_str(time):
    """Returns the hour and minute string
    representation of the provided time.
    """

    return '{}:{}'.format(time.hour, time.minute)


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


class Configuration(DSCMS4Model, CustomerModel):
    """Customer configuration for charts."""

    name = CharField(255)
    description = CharField(255, null=True, default=None)
    font = EnumField(Font)
    portrait = BooleanField(default=False)
    touch = BooleanField()
    design = EnumField(Design)
    effects = BooleanField()
    ticker_speed = SmallIntegerField()
    colors = ForeignKeyField(Colors, db_column='colors')
    title_size = SmallIntegerField()
    text_size = SmallIntegerField()
    logo = IntegerField()           # File
    background = IntegerField()     # File
    dummy_picture = IntegerField()  # File
    hide_cursor = BooleanField(default=True)
    rotation = SmallIntegerField(default=0)
    email_form = BooleanField()
    volume = SmallIntegerField()

    @classmethod
    def from_dict(cls, dictionary, customer=None):
        """Creates a new configuration from the provided
        dictionary for the respective customer.
        """
        configuration = super().from_dict(dictionary)
        configuration.customer = customer
        configuration.colors = Colors.from_dict(dictionary.get('colors', {}))
        yield configuration

        for ticker_dict in dictionary.get('tickers', ()):
            yield Ticker.from_dict(ticker_dict, configuration=configuration)

        for backlight in Backlight.from_dict(
                dictionary.get('backlight', {}), configuration=configuration):
            yield backlight

    def to_dict(self):
        """Converts the configuration into a JSON-like dictionary."""
        dictionary = super().to_dict(ignore=self.__class__.colors)
        dictionary['colors'] = self.colors.to_dict()
        dictionary['tickers'] = Ticker.list_for(self)
        dictionary['backlight'] = Backlight.dict_for(self)
        return dictionary

    def delete_instance(self):
        """Deletes this instance."""
        self.colors.delete_instance()

        for ticker in Ticker.by_configuration(self):
            ticker.delete_instance()

        for backlight in Backlight.by_configuration(self):
            backlight.delete_instance()

        return super().delete_instance()


class Ticker(DSCMS4Model):
    """Tickers of the respective configuration."""

    configuration = ForeignKeyField(Configuration, db_column='configuration')
    typ = EnumField(TickerTypes, db_column='type')
    text = TextField()

    @classmethod
    def from_dict(cls, dictionary, configuration=None):
        """Creates a new ticker for the respective
        configuration from the provided dictionary.
        """
        ticker = super().from_dict(dictionary)
        ticker.configuration = configuration
        return ticker

    @classmethod
    def by_configuration(cls, configuration):
        """Yields backlight settings for the respective configuration."""
        return cls.select().where(cls.configuration == configuration)

    @classmethod
    def list_for(cls, configuration):
        """Returns a list of ticker settings
        for the respective configuration.
        """
        return [tkr.to_dict() for tkr in cls.by_configuration(configuration)]


class Backlight(DSCMS4Model):
    """Backlight beightness settings of the respective configuration."""

    configuration = ForeignKeyField(Configuration, db_column='configuration')
    time = TimeField()
    value = SmallIntegerField()     # Brightness in percent.

    @classmethod
    def from_dict(cls, dictionary, configuration=None):
        """Yields new records from the provided dictionary."""
        for timestamp, percent in dictionary.items():
            record = super().from_dict({'time': timestamp, 'value': percent})
            record.configuration = configuration
            yield record

    @classmethod
    def by_configuration(cls, configuration):
        """Yields backlight settings for the respective configuration."""
        return cls.select().where(cls.configuration == configuration)

    @classmethod
    def dict_for(cls, configuration):
        """Returns a dictionary of backlight settings
        for the respective configuration.
        """
        dictionary = {}

        for backlight in cls.by_configuration(configuration):
            dictionary.update(backlight.to_dict())

        return dictionary

    @property
    def percent(self):
        """Returns the percentage as an integer."""
        return percentage(self.value)

    @percent.setter
    def percent(self, value):
        """Sets the percentage."""
        self.value = percentage(value)

    def to_dict(self):
        """Returns the backlight as dictionary."""
        return {stripped_time_str(self.time): self.percent}


MODELS = (Colors, Configuration, Ticker, Backlight)
