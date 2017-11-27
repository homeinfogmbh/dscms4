"""Terminal content management."""

from peewee import DoesNotExist
from terminallib import Terminal
from wsgilib import routed

from his.api.handlers import service, AuthorizedService

from dscms4.orm.content.group import TerminalBaseChart, TerminalConfiguration,\
    TerminalMenu, TerminalTicker

from .common import ContentHandler

__all__ = ['TerminalContent']


@routed('/content/terminal/<tid:int>/[type]')
class TerminalContent(ContentHandler):
    """Handles content associated with terminals."""

    BASE_CHART = TerminalBaseChart
    CONFIGURATION = TerminalConfiguration
    MENU = TerminalMenu
    TICKER = TerminalTicker

    @property
    def container(self):
        """Returns the respective terminal."""
        try:
            return Terminal.get(
                (Terminal.tid == self.vars['tid'])
                & (Terminal.customer == self.customer))
        except DoesNotExist:
            raise NoSuchTerminal() from None
