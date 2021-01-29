"""Digital signage deployments as members in groups."""

from flask import request

from cmslib import GroupMemberDeployment
from cmslib import get_deployment
from cmslib import get_group
from cmslib import get_group_member_deployment
from cmslib import get_group_member_deployments
from his import authenticated, authorized, require_json
from wsgilib import JSON, JSONMessage, get_int


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def list_() -> JSON:
    """Lists group member deployments."""

    return JSON([
        record.to_json() for record
        in get_group_member_deployments(group=get_int('group'))
    ])


@authenticated
@authorized('dscms4')
def get(ident: int) -> JSON:
    """Returns a group member deployment."""

    return JSON(get_group_member_deployment(ident).to_json())


@authenticated
@authorized('dscms4')
@require_json(dict)
def add() -> JSONMessage:
    """Adds a deployment to the respective group."""

    group = get_group(request.json.pop('group'))
    deployment = get_deployment(request.json.pop('deployment'))
    record = GroupMemberDeployment.from_json(request.json, group, deployment)
    record.save()
    return JSONMessage('Group member deployment added.', id=record.id,
                       status=201)


@authenticated
@authorized('dscms4')
def delete(ident: int) -> JSONMessage:
    """Deletes the respective deployment from the group."""

    get_group_member_deployment(ident).delete_instance()
    return JSONMessage('Group member deployment deleted.', status=200)


ROUTES = [
    ('GET', '/group/deployment', list_),
    ('GET', '/group/deployment/<int:ident>', get),
    ('POST', '/group/deployment', add),
    ('DELETE', '/group/deployment/<int:ident>', delete)
]
