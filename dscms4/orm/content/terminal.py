"""Content assigned to Terminals."""

from peewee import DoesNotExist, Model, ForeignKeyField

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


class TerminalContent(DSCMS4Model):
    """Common abstract content mapping."""

    terminal = ForeignKeyField(Terminal, db_column='terminal')
    content = None

    @classmethod
    def _add(cls, terminal, content):
        """Adds a new association of content with a terminal."""
        mapping = cls()
        mapping.terminal = terminal
        mapping.content = content
        return mapping

    @classmethod
    def add(cls, terminal, content):
        """Adds a new association of content with
        a terminal iff it does not yet exist.
        """
        try:
            return cls.get(
                (cls.terminal == terminal)
                & (cls.content == content))
        except DoesNotExist:
            return cls._add(terminal, content)


class TerminalBaseChart(Model, TerminalContent):
    """Association of a base chart with a terminal."""

    class Meta:
        db_table = 'terminal_base_chart'

    content = ForeignKeyField(BaseChart, db_column='base_chart')


class TerminalConfiguration(Model, TerminalContent):
    """Association of a configuration with a terminal."""

    class Meta:
        db_table = 'terminal_configuration'

    content = ForeignKeyField(Configuration, db_column='configuration')


class TerminalMenu(Model, TerminalContent):
    """Association of a menu with a terminal."""

    class Meta:
        db_table = 'terminal_menu'

    content = ForeignKeyField(Menu, db_column='menu')


class TerminalTicker(Model, TerminalContent):
    """Association of a ticker with a terminal."""

    class Meta:
        db_table = 'terminal_ticker'

    content = ForeignKeyField(Ticker, db_column='ticker')
