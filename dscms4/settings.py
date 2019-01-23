"""Per-customer settings interface."""

from flask import request

from cmslib.messages.settings import SETTINGS_SAVED
from cmslib.orm.settings import Settings
from his import CUSTOMER, admin, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get_settings():
    """Gets the customer's settings."""

    settings = Settings.for_customer(CUSTOMER.id)
    return JSON(settings.to_json())


@authenticated
@authorized('dscms4')
@admin
def set_settings():
    """Sets the customer's settings."""

    settings = Settings.for_customer(CUSTOMER.id)
    settings.patch_json(request.json)
    settings.save()
    return SETTINGS_SAVED


ROUTES = (
    ('GET', '/settings', get_settings, 'get_settings'),
    ('POST', '/settings', set_settings, 'set_settings'))
