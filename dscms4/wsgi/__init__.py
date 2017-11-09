"""WSGI handlers."""

from .chart import HANDLERS as CHART_HANDLERS
from .configuration import Configuration
from .group import HANDLERS as GROUP_HANDLERS
from .media import Media
from .menu import Menu
from .ticker import Ticker

__all__ = ['HANDLERS']


HANDLERS = {
    'chart': CHART_HANDLERS,
    'configuration': Configuration,
    'group': GROUP_HANDLERS,
    'media': Media,
    'menu': Menu,
    'ticker': Ticker}
