"""Per-customer settings interface."""

from flask import request

from cmslib import Settings
from his import CUSTOMER, admin, authenticated, authorized
from wsgilib import JSON, JSONMessage, require_json


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get() -> JSON:
    """Gets the customer's settings."""

    return JSON(Settings.for_customer(CUSTOMER.id).to_json())


@authenticated
@authorized('dscms4')
@admin
@require_json(dict)
def patch() -> JSONMessage:
    """Sets the customer's settings."""

    settings = Settings.for_customer(CUSTOMER.id)
    settings.patch_json(request.json)
    settings.save()
    return JSONMessage('Settings saved.', status=200)


ROUTES = [
    ('GET', '/settings', get),
    ('POST', '/settings', patch),
    ('PATCH', '/settings', patch)
]
