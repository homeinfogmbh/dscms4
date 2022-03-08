"""Time schedules."""

from flask import request

from cmslib import Schedule, get_schedule, get_schedules
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage, require_json


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists the customer's schedules."""

    return JSON([
        schedule.to_json() for schedule in get_schedules(CUSTOMER.id)
    ])


@authenticated
@authorized('dscms4')
def get(ident) -> JSON:
    """Returns a specific schedule."""

    return JSON(get_schedule(ident, CUSTOMER.id).to_json())


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds a schedule."""

    schedule = Schedule.from_json(request.json)
    schedule.save()
    return JSONMessage('Added schedule.', id=schedule.id, status=201)


@authenticated
@authorized('dscms4')
@require_json(dict)
def patch(ident: int) -> JSONMessage:
    """Patches a schedule."""

    schedule = get_schedule(ident, CUSTOMER.id)
    schedule = schedule.patch_json(request.json)
    schedule.save()
    return JSONMessage('Schedule patched.', status=200)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes a schedule."""

    get_schedule(ident, CUSTOMER.id).delete_instance()
    return JSONMessage('Schedule deleted.', status=200)


ROUTES = [
    ('GET', '/schedule', list_),
    ('GET', '/schedule/<int:ident>', get),
    ('POST', '/schedule', add),
    ('PATCH', '/schedule/<int:ident>', patch),
    ('DELETE', '/schedule/<int:ident>', delete)
]
