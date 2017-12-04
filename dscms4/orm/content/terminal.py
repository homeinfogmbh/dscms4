"""Content assigned to Terminals."""

from peewee import DoesNotExist, ForeignKeyField

from terminallib import Terminal

from dscms4.orm.charts import BaseChart
from dscms4.orm.common import DSCMS4Model
from dscms4.orm.configuration import Configuration
from dscms4.orm.menu import Menu
from dscms4.orm.ticker import Ticker

__all__ = [
    'TerminalBaseChart',
    'TerminalConfiguration',
    'TerminalMenu',
    'TerminalTicker']


class TerminalContent:
    """Common abstract content mapping."""

    terminal = ForeignKeyField(Terminal, db_column='terminal')


class TerminalBaseChart(DSCMS4Model, TerminalContent):
    """Association of a base chart with a terminal."""

    class Meta:
        db_table = 'terminal_base_chart'

    content = ForeignKeyField(BaseChart, db_column='base_chart')


class TerminalConfiguration(DSCMS4Model, TerminalContent):
    """Association of a configuration with a terminal."""

    class Meta:
        db_table = 'terminal_configuration'

    content = ForeignKeyField(Configuration, db_column='configuration')


class TerminalMenu(DSCMS4Model, TerminalContent):
    """Association of a menu with a terminal."""

    class Meta:
        db_table = 'terminal_menu'

    content = ForeignKeyField(Menu, db_column='menu')


class TerminalTicker(DSCMS4Model, TerminalContent):
    """Association of a ticker with a terminal."""

    class Meta:
        db_table = 'terminal_ticker'

    content = ForeignKeyField(Ticker, db_column='ticker')
