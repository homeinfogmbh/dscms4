"""ComCat account content management."""

from peewee import DoesNotExist
from wsgilib import routed

from his.api.handlers import service, AuthorizedService

from dscms4.orm.content.comcat_account import ComCatAccountBaseChart, \
    ComCatAccountConfiguration, ComCatAccountMenu, ComCatAccountTicker
from dscms4.orm.group import Group

from .common import ContentHandler

__all__ = ['ComCatAccountContent']


@routed('/content/group/<id:int>/[type]')
class ComCatAccountContent(ContentHandler):
    """Handles content associated with ComCat accounts."""

    BASE_CHART = ComCatAccountBaseChart
    CONFIGURATION = ComCatAccountConfiguration
    MENU = ComCatAccountMenu
    TICKER = ComCatAccountTicker

    @property
    def container(self):
        """Returns the respective ComCat account."""
        try:
            return ComCatAccount.get(
                (ComCatAccount.id == self.vars['id'])
                & (ComCatAccount.customer == self.customer))
        except DoesNotExist:
            raise NoSuchGroup() from None
