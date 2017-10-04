"""Configurations, colors, tickers and brightness settings."""

from datetime import datetime
from enum import Enum

from peewee import ForeignKeyField, TimeField, DecimalField, IntegerField, \
    SmallIntegerField, CharField, BooleanField, TextField

from peeweeplus import JSONModel, EnumField

from .common import DSCMS4Model, CustomerModel

__all__ = [
    'create_tables',
    'Colors',
    'Configuration',
    'Backlight',
    'MODELS']


def percentage(value):
    """Returns the percentage of a decimal number."""

    if 0 <= value <= 100:
        return value

    raise ValueError('Invalid percentage: {}.'.format(value))


def stripped_time_str(time):
    """Returns the hour and minute string
    representation of the provided time.
    """

    return '{}:{}'.format(time.hour, time.minute)


def create_tables(fail_silently=True):
    """Creates the tables of this module."""

    for model in MODELS:
        model.create_table(fail_silently=fail_silently)


class TickerTypes(Enum):
    """Valid ticker types."""

    TEXT = 'text'
    RSS = 'RSS'
    STOCK_PRICES = 'stock prices'


class Colors(JSONModel, DSCMS4Model):
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


class Configuration(JSONModel, CustomerModel):
    """Customer configuration for charts."""

    name = CharField(255)
    description = CharField(255, null=True, default=None)
    font = CharField(16)
    portrait = BooleanField(default=False)
    touch = BooleanField()
    design = CharField(8)
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
    def from_dict(cls, dictionary, customer):
        """Creates a new configuration from the provided
        dictionary for the respective customer.
        """
        record = super().from_dict(dictionary)
        record.customer = customer
        record.colors = Colors.from_dict(dictionary.get('colors', {}))
        record.save()

        for ticker in dictionary.get('tickers', []):
            ticker = Ticker.from_dict(ticker, record)
            ticker.save()

        for backlight in Backlight.from_dict(
                dictionary.get('backlight', {}), record):
            backlight.save()

        return record

    def to_dict(self):
        """Converts the configuration into a JSON-like dictionary."""
        dictionary = super().to_dict(blacklist=ForeignKeyField)
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


class Ticker(JSONModel, DSCMS4Model):
    """Tickers of the respective configuration."""

    configuration = ForeignKeyField(Configuration, db_column='configuration')
    typ = EnumField(TickerTypes, db_column='type')
    text = TextField()

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


class Backlight(JSONModel, DSCMS4Model):
    """Backlight beightness settings of the respective configuration."""

    configuration = ForeignKeyField(Configuration, db_column='configuration')
    time = TimeField()
    value = DecimalField(3, 2)

    @classmethod
    def add(cls, configuration, time, value=None, percent=None):
        """Adds a new backlight setting."""
        record = cls()
        record.configuration = configuration
        record.time = time

        if value is not None and percent is not None:
            raise ValueError('Must specify either value or percent.')
        elif value is not None:
            record.value = value
        elif percent is not None:
            record.percent = percent
        else:
            raise ValueError('Must specify either value or percent.')

        record.save()
        return record

    @classmethod
    def by_configuration(cls, configuration):
        """Yields backlight settings for the respective configuration."""
        return cls.select().where(cls.configuration == configuration)

    @classmethod
    def from_dict(cls, dictionary, configuration):
        """Yields new records from the provided dictionary."""
        for timestamp, percent in dictionary.items():
            record = cls()
            record.configuration = configuration
            record.time = datetime.strptime(timestamp, '%H:%M').time()
            record.percent = percent
            yield record

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
        return percentage(int(self.value * 100))

    @percent.setter
    def percent(self, value):
        """Sets the percentage."""
        self.value = percentage(value) / 100

    def to_dict(self):
        """Returns the backlight as dictionary."""
        return {stripped_time_str(self.time): self.percent}


MODELS = (Colors, Configuration, Ticker, Backlight)
