"""Group content management."""

from peewee import DoesNotExist
from wsgilib import routed

from his.api.handlers import service, AuthorizedService

from dscms4.orm.content.group import GroupBaseChart, GroupConfiguration, \
    GroupMenu, GroupTicker
from dscms4.orm.group import Group

from .common import ContentHandler

__all__ = ['GroupContent']


@routed('/content/group/<id:int>/[type]')
class GroupContent(ContentHandler):
    """Handles content associated with groups."""

    BASE_CHART = GroupBaseChart
    CONFIGURATION = GroupConfiguration
    MENU = GroupMenu
    TICKER = GroupTicker

    @property
    def container(self):
        """Returns the respective group."""
        try:
            return Group.get(
                (Group.id == self.vars['id'])
                & (Group.customer == self.customer))
        except DoesNotExist:
            raise NoSuchGroup() from None
