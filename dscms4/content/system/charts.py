"""Management of charts in digital signage systems."""

from cmslib.functions.charts import get_chart
from cmslib.functions.system import get_system
from cmslib.messages.content import CONTENT_ADDED
from cmslib.messages.content import CONTENT_DELETED
from cmslib.messages.content import CONTENT_PATCHED
from cmslib.messages.content import NO_SUCH_CONTENT
from cmslib.orm.charts import BaseChart
from cmslib.orm.content.system import SystemBaseChart
from his import CUSTOMER, JSON_DATA, authenticated, authorized
from terminallib import Location, System
from wsgilib import JSON


__all__ = ['ROUTES']


def list_sbc(ident):
    """Yields the system base charts of the
    current customer for the respective termianl.
    """

    term_join = SystemBaseChart.system == System.id
    location_join = System.location == Location.id
    bc_join = SystemBaseChart.base_chart == BaseChart.id
    return SystemBaseChart.select().join(
        System, join_type='LEFT', on=term_join).join(
        Location, join_type='LEFT', on=location_join).join(
        BaseChart, join_type='LEFT', on=bc_join).where(
            (Location.customer == CUSTOMER.id) & (System.id == ident)
            & (BaseChart.trashed == 0))


def get_tbc(system_id, ident):
    """Returns the respective system base chart."""

    try:
        return SystemBaseChart.select().join(System).join(Location).where(
            (SystemBaseChart.id == ident)
            & (System.id == system_id)
            & (Location.customer == CUSTOMER.id)).get()
    except SystemBaseChart.DoesNotExist:
        raise NO_SUCH_CONTENT


@authenticated
@authorized('dscms4')
def get(system_id):
    """Returns a list of IDs of the charts in the respective system."""

    return JSON([tbc.to_json() for tbc in list_sbc(system_id)])


@authenticated
@authorized('dscms4')
def add(system_id, ident):
    """Adds the chart to the respective system."""

    system = get_system(system_id)
    base_chart = get_chart(ident).base
    sbc = SystemBaseChart.from_json(JSON_DATA, system, base_chart)
    sbc.save()
    return CONTENT_ADDED.update(id=sbc.id)


@authenticated
@authorized('dscms4')
def patch(system_id, ident):
    """Adds the chart to the respective system."""

    sbc = get_sbc(system_id, ident)
    sbc.patch_json(JSON_DATA)
    sbc.save()
    return CONTENT_PATCHED


@authenticated
@authorized('dscms4')
def delete(system_id, ident):
    """Deletes the chart from the respective system."""

    sbc = get_sbc(system_id, ident)
    sbc.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/system/<int:system_id>/chart', get, 'list_system_charts'),
    ('POST', '/content/system/<int:system_id>/chart/<int:ident>', add,
     'add_system_chart'),
    ('PATCH', '/content/system/<int:system_id>/chart/<int:ident>', patch,
     'patch_system_chart'),
    ('DELETE', '/content/system/<int:system_id>/chart/<int:ident>', delete,
     'delete_system_chart'))
