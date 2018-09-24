"""Per-customer settings interface."""

from flask import request

from his import CUSTOMER, admin, authenticated, authorized
from wsgilib import JSON

from dscms4.messages.settings import SettingsSaved
from dscms4.orm.settings import Settings


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
    settings.patch(request.json4)
    settings.save()
    return SettingsSaved()


ROUTES = (
    ('/GET', '/settings', get_settings, 'get_settings'),
    ('/POST', '/settings', set_settings, 'set_settings'))
