"""Groups tree endpoint."""

from __future__ import annotations
from typing import Iterator, Union

from peewee import JOIN, ModelSelect

from functoolsplus import coerce
from hwdb import Deployment
from mdb import Address, Company, Customer

from cmslib import BaseChart
from cmslib import Group
from cmslib import GroupBaseChart
from cmslib import GroupConfiguration
from cmslib import GroupMemberDeployment
from cmslib import GroupMenu
from cmslib import get_group
from cmslib import get_trashed
from his import CUSTOMER, authenticated, authorized
from wsgilib import JSON


__all__ = ['ROUTES']


def get_deployments(ids: Iterator[Union[Deployment, int]]) -> ModelSelect:
    """Selects deployments from the database."""

    return Deployment.select(Deployment, Customer, Company, Address).join(
        Customer).join(Company).join_from(
        Deployment, Address, on=Deployment.address == Address.id).where(
        Deployment.id << set(ids)
    )


def get_root_groups() -> ModelSelect:
    """Selects root-level groups."""

    return Group.select().where(
        (Group.customer == CUSTOMER.id) & (Group.parent >> None))


def get_groups_tree() -> Iterator[GroupContent]:
    """Returns the management tree."""

    for root_group in get_root_groups():
        yield GroupContent(root_group)


@authenticated
@authorized('dscms4')
def groups_tree() -> JSON:
    """Lists the groups."""

    return JSON([group.to_json() for group in get_groups_tree()])


@authenticated
@authorized('dscms4')
def groups_subtree(gid: int) -> JSON:
    """Lists the groups."""

    group_content = GroupContent(get_group(gid))
    return JSON(group_content.to_json(recursive=False))


class GroupContent:
    """Represents content of a group."""

    def __init__(self, group: Group):
        """Sets the respective group."""
        self.group = group

    @property
    def children(self) -> Iterator[GroupContent]:
        """Yields children of this group."""
        for group in Group.select().where(Group.parent == self.group):
            yield GroupContent(group)

    @property
    def charts(self) -> Iterator[dict]:
        """Yields the group's charts."""
        bc_join = GroupBaseChart.base_chart == BaseChart.id

        for group_base_chart in GroupBaseChart.select().join(
                BaseChart, join_type=JOIN.LEFT_OUTER, on=bc_join).where(
                    (GroupBaseChart.group == self.group) & get_trashed()):
            yield group_base_chart.to_json()

    @property
    def configurations(self) -> Iterator[dict]:
        """Yields the group's configurations."""
        for group_configuration in GroupConfiguration.select().where(
                GroupConfiguration.group == self.group):
            yield group_configuration.to_json()

    @property
    def menus(self) -> Iterator[dict]:
        """Yields the group's menus."""
        for group_menu in GroupMenu.select().where(
                GroupMenu.group == self.group):
            yield group_menu.to_json()

    @property
    def content(self) -> dict:
        """Returns content."""
        return {
            'charts': list(self.charts),
            'configurations': list(self.configurations),
            'menus': list(self.menus)
        }

    @property
    @coerce(get_deployments)
    def deployments(self) -> Iterator[Deployment]:
        """Yields deployments of this group."""
        for group_member_deployment in GroupMemberDeployment.select().where(
                GroupMemberDeployment.group == self.group):
            yield group_member_deployment.deployment

    def to_json(self, recursive: bool = True) -> dict:
        """Recursively converts the group content into a JSON-ish dict."""
        json = self.group.to_json(parent=False, skip=('customer',))

        if recursive:
            children = [
                group.to_json(recursive=True) for group in self.children]
        else:
            children = [
                group.group.to_json(parent=False, skip=('customer',))
                for group in self.children]

        json['children'] = children
        json['content'] = self.content
        json['deployments'] = [
            deployment.to_json() for deployment in self.deployments]
        return json


ROUTES = [
    ('GET', '/grouptree', groups_tree),
    ('GET', '/grouptree/<int:gid>', groups_subtree)
]
