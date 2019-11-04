"""Base chart related schedules."""

from cmslib.messages.schedule import SCHEDULE_ADDED
from cmslib.messages.schedule import SCHEDULE_PATCHED
from cmslib.messages.schedule import SCHEDULE_DELETED

from cmslib.functions.base_chart_schedule import get_base_chart_schedule
from cmslib.orm.base_chart_schedule import BaseChartSchedule
from his import CUSTOMER, JSON_DATA, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_():
    """Lists the customer's schedules."""

    bc_schedules = BaseChartSchedule.select().where(
        BaseChartSchedule.customer == CUSTOMER.id)
    return JSON([bc_schedule.to_json() for bc_schedule in bc_schedules])


@authenticated
@authorized('dscms4')
def get(ident):
    """Returns a specific schedule."""

    return get_base_chart_schedule(ident).to_json()


@authenticated
@authorized('dscms4')
def add():
    """Adds a schedule."""

    json = dict(JSON_DATA)
    bc_schedule = BaseChartSchedule.from_json(json)
    bc_schedule.save()
    return SCHEDULE_ADDED.update(id=bc_schedule.id)


@authenticated
@authorized('dscms4')
def patch(ident):
    """Patches a schedule."""

    bc_schedule = get_base_chart_schedule(ident)
    json = dict(JSON_DATA)
    bc_schedule = bc_schedule.patch_json(json)
    bc_schedule.save()
    return SCHEDULE_PATCHED


@authenticated
@authorized('dscms4')
def delete(ident):
    """Deletes a schedule."""

    bc_schedule = get_base_chart_schedule(ident)
    bc_schedule = bc_schedule.delete_instance()
    return SCHEDULE_DELETED


ROUTES = (
    ('GET', '/base-chart-schedule', list_),
    ('GET', '/base-chart-schedule/<int:ident>', get),
    ('POST', '/base-chart-schedule', add),
    ('PATCH', '/base-chart-schedule/<int:ident>', patch),
    ('DELETE', '/base-chart-schedule/<int:ident>', delete)
)
