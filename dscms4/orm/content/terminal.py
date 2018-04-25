"""Content assigned to Terminals."""

from peewee import ForeignKeyField

from terminallib import Terminal

from dscms4.orm.charts import BaseChart
from dscms4.orm.common import DSCMS4Model
from dscms4.orm.configuration import Configuration
from dscms4.orm.menu import Menu
from dscms4.orm.configuration import Ticker

__all__ = [
    'TerminalBaseChart',
    'TerminalConfiguration',
    'TerminalMenu',
    'TerminalTicker',
    'MODELS']


class _TerminalContent(DSCMS4Model):
    """Common abstract content mapping."""

    terminal = ForeignKeyField(
        Terminal, column_name='terminal', on_delete='CASCADE')


class TerminalBaseChart(_TerminalContent):
    """Association of a base chart with a terminal."""

    class Meta:
        table_name = 'terminal_base_chart'

    content = ForeignKeyField(
        BaseChart, column_name='base_chart', on_delete='CASCADE')


class TerminalConfiguration(_TerminalContent):
    """Association of a configuration with a terminal."""

    class Meta:
        table_name = 'terminal_configuration'

    content = ForeignKeyField(
        Configuration, column_name='configuration', on_delete='CASCADE')


class TerminalMenu(_TerminalContent):
    """Association of a menu with a terminal."""

    class Meta:
        table_name = 'terminal_menu'

    content = ForeignKeyField(Menu, column_name='menu', on_delete='CASCADE')


class TerminalTicker(_TerminalContent):
    """Association of a ticker with a terminal."""

    class Meta:
        table_name = 'terminal_ticker'

    content = ForeignKeyField(
        Ticker, column_name='ticker', on_delete='CASCADE')


MODELS = (
    TerminalBaseChart, TerminalConfiguration, TerminalMenu, TerminalTicker)
