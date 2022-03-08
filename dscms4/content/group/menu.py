"""Management of menus in groups."""

from flask import request

from cmslib import GroupMenu
from cmslib import get_group
from cmslib import get_group_menu
from cmslib import get_group_menus
from cmslib import get_menu
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON, JSONMessage, get_int, require_json


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists the respective group menus."""

    return JSON([record.to_json() for record in get_group_menus(
        CUSTOMER.id, group=get_int('group')
    )])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Lists the respective group menus."""

    return JSON(get_group_menu(ident, CUSTOMER.id).to_json(cascade=True))


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds the menu to the respective group."""

    group = get_group(request.json.pop('group'), CUSTOMER.id)
    menu = get_menu(request.json.pop('menu'), CUSTOMER.id)
    record = GroupMenu(group=group, menu=menu)
    record.save()
    return JSONMessage('Group menu added.', id=record.id, status=201)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes the menu from the respective group."""

    get_group_menu(ident, CUSTOMER.id).delete_instance()
    return JSONMessage('Group menu deleted.', status=200)


ROUTES = [
    ('GET', '/content/group/menu', list_),
    ('GET', '/content/group/menu/<int:ident>', get),
    ('POST', '/content/group/menu', add),
    ('DELETE', '/content/group/menu/<int:ident>', delete)
]
