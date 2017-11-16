"""WSGI handlers."""

from .chart import HANDLERS as CHART_HANDLERS
from .configuration import ConfigurationHandler
from .group import HANDLERS as GROUP_HANDLERS
from .media import MediaHandler
from .menu import MenuHandler
from .ticker import TickerHandler

__all__ = ['mk_router']


def mk_router(root):
    """Generates a router for the respective root."""

    return Router(
        (Route('{}/chart/[id:int]'), CHART_HANDLERS),
        (Route('{}/configuration/[id:int]'), ConfigurationHandler),
        (Route('{}/group/[id:int]'), GROUP_HANDLERS),
        (Route('{}/media/[id:int]'), MediaHandler),
        (Route('{}/menu/[id:int]'), MenuHandler),
        (Route('{}/ticker/[id:int]'), TickerHandler))
