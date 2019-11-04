"""Time schedules."""

from cmslib.messages.schedule import SCHEDULE_ADDED
from cmslib.messages.schedule import SCHEDULE_PATCHED
from cmslib.messages.schedule import SCHEDULE_DELETED

from cmslib.functions.schedule import get_schedule
from cmslib.orm.schedule import Schedule
from his import CUSTOMER, JSON_DATA, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_():
    """Lists the customer's schedules."""

    schedules = Schedule.select().where(Schedule.customer == CUSTOMER.id)
    return JSON([schedule.to_json() for schedule in schedules])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns a specific schedule."""

    return get_schedule(ident).to_json()


@authenticated
@authorized('dscms4')
def add():
    """Adds a schedule."""

    json = dict(JSON_DATA)
    schedule = Schedule.from_json(json)
    schedule.save()
    return SCHEDULE_ADDED.update(id=schedule.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches a schedule."""

    schedule = get_schedule(ident)
    json = dict(JSON_DATA)
    schedule = schedule.patch_json(json)
    schedule.save()
    return SCHEDULE_PATCHED


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes a schedule."""

    schedule = get_schedule(ident)
    schedule = schedule.delete_instance()
    return SCHEDULE_DELETED


ROUTES = (
    ('GET', '/schedule', list_),
    ('GET', '/schedule/<int:ident>', get),
    ('POST', '/schedule', add),
    ('PATCH', '/schedule/<int:ident>', patch),
    ('DELETE', '/schedule/<int:ident>', delete)
)
