"""Configurations controller."""

from datetime import datetime

from flask import request

from his import authenticated, authorized
from wsgilib import JSON

from dscms4.messages.configuration import NoSuchConfiguration, \
    ConfigurationAdded, ConfigurationPatched, ConfigurationDeleted
from dscms4.orm.configuration import TIME_FORMAT, Colors, Configuration, \
    Ticker, Backlight


__all__ = ['get_configuration', 'ROUTES']


def get_configuration(ident):
    """Returns the respective configuration."""

    try:
        return Configuration.cget(Configuration.id == ident)
    except Configuration.DoesNotExist:
        raise NoSuchConfiguration()


@authenticated
@authorized('dscms4')
def list_():
    """Returns a list of IDs of the customer's configurations."""

    return JSON([
        configuration.to_dict() for configuration
        in Configuration.cselect().where(True)])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective configuration."""

    return JSON(get_configuration(ident).to_dict())


@authenticated
@authorized('dscms4')
def add():
    """Adds a new configuration."""

    json = request.json
    colors = json.pop('colors', {})
    tickers = json.pop('tickers', ())
    backlight = json.pop('backlight', {})
    # Create related colors first.
    colors = Colors.from_json(colors)
    colors.save()
    configuration = Configuration.from_dict(json, colors)
    configuration.save()

    # Create related tickers.
    for ticker in tickers:
        ticker = Ticker.from_json(ticker, configuration)
        ticker.save()

    # Create related backlight records.
    for time, brightness in backlight.items():
        time = datetime.strptime(time, TIME_FORMAT).time()
        backlight = {'time': time, 'brightness': brightness}
        backlight = Backlight.from_json(backlight, configuration)
        backlight.save()

    return ConfigurationAdded(id=configuration.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Modifies an existing configuration."""

    json = request.json
    colors = json.pop('colors', None)
    tickers = json.pop('tickers', None)
    backlight = json.pop('backlight', None)
    configuration = get_configuration(ident)
    configuration.patch(json)
    configuration.save()

    # Patch related colors.
    if colors is not None:
        configuration.colors.patch_json(colors)
        configuration.colors.save()

    # Update related tickers.
    if tickers is not None:
        for ticker in configuration.tickers:
            ticker.delete_instance()

        for ticker in tickers:
            ticker = Ticker.from_json(ticker, configuration)
            ticker.save()

    # Update backlight settings.
    if backlight is not None:
        for backlight_ in configuration.backlights:
            backlight_.delete_instance()

        for backlight in Backlight.from_json(backlight, configuration):
            backlight.save()

    return ConfigurationPatched()


@authenticated
@authorized('dscms4')
def delete(ident):
    """Modifies an existing configuration."""

    get_configuration(ident).delete_instance()
    return ConfigurationDeleted()


ROUTES = (
    ('GET', '/configuration', list_, 'list_configurations'),
    ('GET', '/configuration/<int:ident>', get, 'get_configuration'),
    ('POST', '/configuration', add, 'add_configuration'),
    ('PATCH', '/configuration/<int:ident>', patch, 'patch_configuration'),
    ('DELETE', '/configuration/<int:ident>', delete, 'delete_configuration'))
