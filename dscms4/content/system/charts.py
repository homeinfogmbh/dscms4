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
from terminallib import Deployment, System
from wsgilib import JSON


__all__ = ['ROUTES']


def list_sbc(ident):
    """Yields the system base charts of the
    current customer for the respective termianl.
    """

    term_join = SystemBaseChart.system == System.id
    deployment_join = System.deployment == Deployment.id
    bc_join = SystemBaseChart.base_chart == BaseChart.id
    return SystemBaseChart.select().join(
        System, join_type='LEFT', on=term_join).join(
            Deployment, join_type='LEFT', on=deployment_join).join(
                BaseChart, join_type='LEFT', on=bc_join).where(
                    (System.id == ident)
                    & (Deployment.customer == CUSTOMER.id)
                    & (BaseChart.trashed == 0))


def get_sbc(system_id, ident):
    """Returns the respective system base chart."""

    try:
        return SystemBaseChart.select().join(System).join(Deployment).where(
            (SystemBaseChart.id == ident)
            & (System.id == system_id)
            & (Deployment.customer == CUSTOMER.id)).get()
    except SystemBaseChart.DoesNotExist:
        raise NO_SUCH_CONTENT


@authenticated
@authorized('dscms4')
def get(system):
    """Returns a list of IDs of the charts in the respective system."""

    return JSON([sbc.to_json() for sbc in list_sbc(system)])


@authenticated
@authorized('dscms4')
def add(system, chart):
    """Adds the chart to the respective system."""

    system = get_system(system)
    base_chart = get_chart(chart).base
    sbc = SystemBaseChart.from_json(JSON_DATA, system, base_chart)
    sbc.save()
    return CONTENT_ADDED.update(id=sbc.id)


@authenticated
@authorized('dscms4')
def patch(system, chart):
    """Adds the chart to the respective system."""

    sbc = get_sbc(system, chart)
    sbc.patch_json(JSON_DATA)
    sbc.save()
    return CONTENT_PATCHED


@authenticated
@authorized('dscms4')
def delete(system, chart):
    """Deletes the chart from the respective system."""

    sbc = get_sbc(system, chart)
    sbc.delete_instance()
    return CONTENT_DELETED


ROUTES = (
    ('GET', '/content/system/<int:system>/chart', get),
    ('POST', '/content/system/<int:system>/chart/<int:chart>', add),
    ('PATCH', '/content/system/<int:system>/chart/<int:chart>', patch),
    ('DELETE', '/content/system/<int:system>/chart/<int:chart>', delete)
)
