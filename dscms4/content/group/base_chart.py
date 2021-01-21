"""Management of charts in groups."""

from flask import request

from cmslib.functions.charts import get_base_chart
from cmslib.functions.content import get_group_base_chart
from cmslib.functions.content import get_group_base_charts
from cmslib.functions.group import get_group
from cmslib.orm.content.group import GroupBaseChart
from his import authenticated, authorized,require_json
from wsgilib import JSON, JSONMessage, get_bool, get_int


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists the requested group <> base chart mappings."""

    return JSON([record.to_json() for record in get_group_base_charts(
        deployment=get_int('group'), trashed=get_bool('trashed', None))])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns the requested group <> base chart mapping."""

    return JSON(get_group_base_chart(ident).to_json())


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds a group <> base chart mapping."""

    group = get_group(request.json.pop('group'))
    base_chart = get_base_chart(request.json.pop('baseChart'))
    record = GroupBaseChart.from_json(request.json, group, base_chart)
    record.save()
    return JSONMessage('Group base chart added.', id=record.id, status=201)


@authenticated
@authorized('dscms4')
@require_json(dict)
def patch(ident: int) -> JSONMessage:
    """Patches a group <> base chart mapping, i.e. changes its index."""

    record = get_group_base_chart(ident)
    record.patch_json(request.json)
    record.save()
    return JSONMessage('Group base chart patched.', status=200)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes a group <> base chart mapping."""

    get_group_base_chart(ident).delete_instance()
    return JSONMessage('Group base chart deleted.', status=200)


ROUTES = (
    ('GET', '/content/group/base_chart', list_),
    ('GET', '/content/group/base_chart/<int:ident>', get),
    ('POST', '/content/group/base_chart', add),
    ('PATCH', '/content/group/base_chart/<int:ident>', patch),
    ('DELETE', '/content/group/base_chart/<int:ident>', delete)
)
