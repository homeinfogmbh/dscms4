"""Per-customer settings interface."""

from cmslib.messages.settings import SETTINGS_SAVED
from cmslib.orm.settings import Settings
from his import CUSTOMER, JSON_DATA, admin, authenticated, authorized
from wsgilib import JSON, JSONMessage


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get_settings() -> JSON:
    """Gets the customer's settings."""

    settings = Settings.for_customer(CUSTOMER.id)
    return JSON(settings.to_json())


@authenticated
@authorized('dscms4')
@admin
def set_settings() -> JSONMessage:
    """Sets the customer's settings."""

    json = dict(JSON_DATA)
    settings = Settings.for_customer(CUSTOMER.id)
    settings.patch_json(json)
    settings.save()
    return SETTINGS_SAVED


ROUTES = (
    ('GET', '/settings', get_settings),
    ('POST', '/settings', set_settings)
)
