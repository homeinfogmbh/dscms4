"""Management of charts in groups."""

from flask import request

from cmslib import GroupBaseChart
from cmslib import get_base_chart
from cmslib import get_group
from cmslib import get_group_base_chart
from cmslib import get_group_base_charts
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage, get_int, require_json

from dscms4.fcm import notify_base_chart


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists the requested group <> base chart mappings."""

    return JSON([record.to_json() for record in get_group_base_charts(
        CUSTOMER.id, group=get_int('group')
    )])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the requested group <> base chart mapping."""

    return JSON(get_group_base_chart(ident, CUSTOMER.id).to_json())


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds a group <> base chart mapping."""

    group = get_group(request.json.pop('group'), CUSTOMER.id)
    base_chart = get_base_chart(request.json.pop('baseChart'), CUSTOMER.id)
    record = GroupBaseChart.from_json(request.json, group, base_chart)
    record.save()
    notify_base_chart(base_chart)
    return JSONMessage('Group base chart added.', id=record.id, status=201)


@authenticated
@authorized('dscms4')
@require_json(dict)
def patch(ident: int) -> JSONMessage:
    """Patches a group <> base chart mapping, i.e. changes its index."""

    record = get_group_base_chart(ident, CUSTOMER.id)
    record.patch_json(request.json)
    record.save()
    return JSONMessage('Group base chart patched.', status=200)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes a group <> base chart mapping."""

    get_group_base_chart(ident, CUSTOMER.id).delete_instance()
    return JSONMessage('Group base chart deleted.', status=200)


ROUTES = [
    ('GET', '/content/group/base_chart', list_),
    ('GET', '/content/group/base_chart/<int:ident>', get),
    ('POST', '/content/group/base_chart', add),
    ('PATCH', '/content/group/base_chart/<int:ident>', patch),
    ('DELETE', '/content/group/base_chart/<int:ident>', delete)
]
