"""WSGI handlers."""

from .chart import HANDLERS as CHART_HANDLERS
from .configuration import ConfigurationHandler
from .group import HANDLERS as GROUP_HANDLERS
from .media import MediaHandler
from .menu import MenuHandler
from .ticker import TickerHandler

__all__ = ['HANDLERS']


HANDLERS = {
    'chart': CHART_HANDLERS,
    'configuration': ConfigurationHandler,
    'group': GROUP_HANDLERS,
    'media': MediaHandler,
    'menu': MenuHandler,
    'ticker': TickerHandler}
