"""Configurations controller."""

from datetime import datetime

from his import CUSTOMER, JSON_DATA, authenticated, authorized
from wsgilib import JSON

from dscms4.messages.configuration import NoSuchConfiguration, \
    ConfigurationAdded, ConfigurationPatched, ConfigurationDeleted
from dscms4.orm.configuration import TIME_FORMAT, Colors, Configuration, \
    Ticker, Backlight


__all__ = ['ROUTES', 'list_configurations', 'get_configuration']


def _update_tickers(tickers, configuration, *, delete=True):
    """Updates the respective ticker records."""

    if delete:
        for ticker in configuration.tickers:
            ticker.delete_instance()

    for json in tickers:
        ticker = Ticker.from_json(json, configuration)
        ticker.save()


def _update_backlights(backlights, configuration, *, delete=True):
    """Updates the respective backlight records."""

    if delete:
        for backlight in configuration.backlights:
            backlight.delete_instance()

    for time, brightness in backlights.items():
        time = datetime.strptime(time, TIME_FORMAT).time()
        json = {'time': time, 'brightness': brightness}
        backlight = Backlight.from_json(json, configuration)
        backlight.save()


def list_configurations():
    """Returns the respective configuration."""

    return Configuration.select().where(Configuration.customer == CUSTOMER.id)


def get_configuration(ident):
    """Returns the respective configuration."""

    try:
        return Configuration.get(
            (Configuration.customer == CUSTOMER.id)
            & (Configuration.id == ident))
    except Configuration.DoesNotExist:
        raise NoSuchConfiguration()


@authenticated
@authorized('dscms4')
def list_():
    """Returns a list of IDs of the customer's configurations."""

    return JSON([
        configuration.to_json(fk_fields=False) for configuration
        in list_configurations()])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns the respective configuration."""

    return JSON(get_configuration(ident).to_json(cascade=True))


@authenticated
@authorized('dscms4')
def add():
    """Adds a new configuration."""

    json = JSON_DATA
    colors = json.pop('colors', {})
    tickers = json.pop('tickers', ())
    backlight = json.pop('backlight', {})
    # Create related colors first.
    colors = Colors.from_json(colors)
    colors.save()
    configuration = Configuration.from_json(json, colors)
    configuration.save()
    _update_tickers(tickers, configuration, delete=False)
    _update_backlights(backlight, configuration, delete=False)
    return ConfigurationAdded(id=configuration.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Modifies an existing configuration."""

    json = JSON_DATA
    colors = json.pop('colors', None)
    tickers = json.pop('tickers', None)
    backlight = json.pop('backlight', None)
    configuration = get_configuration(ident)
    configuration.patch_json(json)
    configuration.save()

    # Patch related colors.
    if colors is not None:
        configuration.colors.patch_json(colors)
        configuration.colors.save()

    # Update related tickers.
    if tickers is not None:
        _update_tickers(tickers, configuration)

    # Update backlight settings.
    if backlight is not None:
        _update_backlights(backlight, configuration)

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
