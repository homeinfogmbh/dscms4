"""Digital signage deployments as members in groups."""

from cmslib.functions.group import get_group
from cmslib.messages.group import MEMBER_ADDED
from cmslib.messages.group import MEMBER_DELETED
from cmslib.messages.group import NO_SUCH_MEMBER
from cmslib.orm.group import GroupMemberDeployment
from his import JSON_DATA, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get(gid):
    """Returns the group's members."""

    deployments = []

    for group_member_deployment in GroupMemberDeployment.select().where(
            GroupMemberDeployment.group == get_group(gid)):
        deployments.append(group_member_deployment.deployment.id)

    return JSON(deployments)


@authenticated
@authorized('dscms4')
def add(gid):
    """Adds a deployment to the respective group."""

    group = get_group(gid)
    group_member_deployment = GroupMemberDeployment.from_json(JSON_DATA, group)
    group_member_deployment.save()
    return MEMBER_ADDED.update(id=group_member_deployment.deployment.id)


@authenticated
@authorized('dscms4')
def delete(gid, deployment):
    """Deletes the respective deployment from the group."""

    try:
        group_member_deployment = GroupMemberDeployment.get(
            (GroupMemberDeployment.group == get_group(gid))
            & (GroupMemberDeployment.deployment == deployment))
    except GroupMemberDeployment.DoesNotExist:
        raise NO_SUCH_MEMBER

    group_member_deployment.delete_instance()
    return MEMBER_DELETED


ROUTES = (
    ('GET', '/group/<int:gid>/deployment', get),
    ('POST', '/group/<int:gid>/deployment', add),
    ('DELETE', '/group/<int:gid>/deployment/<int:deployment>', delete)
)
