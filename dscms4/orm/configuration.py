"""Configurations, colors, tickers and brightness settings."""

from contextlib import suppress
from enum import Enum

from peewee import ForeignKeyField, TimeField, IntegerField, \
    SmallIntegerField, CharField, BooleanField, TextField

from peeweeplus import EnumField

from dscms4 import dom
from dscms4.domutil import attachment_dom
from dscms4.orm.common import RelatedKeyField, DSCMS4Model, CustomerModel, \
    RelatedModel

__all__ = [
    'TIME_FORMAT',
    'MODELS',
    'Colors',
    'Configuration',
    'Ticker',
    'Backlight']


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
    JSON_KEYS = {
        'headerBackground': header_background,
        'backgroundLeft': background_left,
        'backgroundRight': background_right,
        'tickerBackground': ticker_background,
        'textBackground': text_background}

    def to_dom(self):
        """Returns an XML DOM of the model."""
        xml = dom.Colors()
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
    JSON_KEYS = {
        'tickerSpeed': ticker_speed, 'titleSize': title_size,
        'textSize': text_size, 'hideCursor': hide_cursor,
        'emailForm': email_form}

    @classmethod
    def from_json(cls, json, colors, **kwargs):
        """Creates a new configuration from the provided
        dictionary for the respective customer.
        """
        configuration = super().from_json(json, **kwargs)
        configuration.colors = colors
        return configuration

    @property
    def files(self):
        """Yields the configuration's files."""
        files = set()

        if self.logo is not None:
            files.add(self.logo)

        if self.background is not None:
            files.add(self.background)

        if self.dummy_picture is not None:
            files.add(self.dummy_picture)

        return files

    @property
    def backlight_dict(self):
        """Returns a backlight settings dictionary for this configuration."""
        backlights = {}

        for backlight in self.backlights:
            with suppress(ValueError):
                backlights.update(backlight.to_json())

        return backlights

    def to_json(self, cascade=False, **kwargs):
        """Converts the configuration into a JSON-like dictionary."""
        json = super().to_json(**kwargs)

        if cascade:
            json['colors'] = self.colors.to_json(
                autofields=False, fk_fields=False, **kwargs)
            json['tickers'] = [
                ticker.to_json(autofields=False, fk_fields=False)
                for ticker in self.tickers]
            json['backlight'] = self.backlight_dict

        return json

    def to_dom(self):
        """Returns an XML DOM of the configuration."""
        xml = dom.Configuration()
        xml.name = self.name
        xml.description = self.description
        xml.font = self.font.value
        xml.portrait = self.portrait
        xml.touch = self.touch
        xml.design = self.design.value
        xml.effects = self.effects
        xml.ticker_speed = self.ticker_speed
        xml.colors = self.colors.to_dom()
        xml.title_size = self.title_size
        xml.text_size = self.text_size
        xml.logo = attachment_dom(self.logo)
        xml.background = attachment_dom(self.background)
        xml.dummy_picture = attachment_dom(self.dummy_picture)
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


class Ticker(RelatedModel):
    """Ticker."""

    configuration = RelatedKeyField(
        Configuration, column_name='configuration', backref='tickers',
        on_delete='CASCADE')
    type_ = EnumField(TickerTypes, column_name='type')
    content = TextField()

    @classmethod
    def from_json(cls, json, configuration, **kwargs):
        """Creates a new ticker from the respective dictionary."""
        ticker = super().from_json(json, **kwargs)
        ticker.configuration = configuration
        return ticker

    def to_dom(self):
        """Returns an XML DOM of the model."""
        xml = dom.Ticker()
        xml.type = self.type_.value
        xml.content_ = self.content     # xml.content is reserved by PyXB.
        return xml


class Backlight(RelatedModel):
    """Backlight beightness settings of the respective configuration."""

    configuration = RelatedKeyField(
        Configuration, column_name='configuration', backref='backlights',
        on_delete='CASCADE')
    time = TimeField()
    brightness = SmallIntegerField()   # Brightness in percent.

    @classmethod
    def from_json(cls, json, configuration, **kwargs):
        """Yields new records from the provided JSON-ish dictionary."""
        backlight = super().from_json(json, **kwargs)
        backlight.configuration = configuration
        return backlight

    @property
    def percent(self):
        """Returns the percentage as an integer."""
        return percentage(self.brightness)

    @percent.setter
    def percent(self, brightness):
        """Sets the percentage."""
        self.brightness = percentage(brightness)

    def to_json(self):
        """Returns the backlight as dictionary."""
        return {self.time.strftime(TIME_FORMAT): self.percent}

    def to_dom(self):
        """Returns an XML DOM of the model."""
        xml = dom.Backlight()
        xml.time = self.time
        xml.brightness = self.brightness
        return xml


MODELS = (Colors, Configuration, Ticker, Backlight)
