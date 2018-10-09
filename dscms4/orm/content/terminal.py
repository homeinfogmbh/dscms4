"""Content assigned to Terminals."""

from peewee import ForeignKeyField, IntegerField

from terminallib import Terminal

from dscms4.orm.charts import ChartMode, BaseChart
from dscms4.orm.common import DSCMS4Model
from dscms4.orm.configuration import Configuration
from dscms4.orm.menu import Menu


__all__ = [
    'TerminalBaseChart',
    'TerminalConfiguration',
    'TerminalMenu',
    'MODELS']


class _TerminalContent(DSCMS4Model):
    """Common abstract content mapping."""

    terminal = ForeignKeyField(
        Terminal, column_name='terminal', on_delete='CASCADE')


class TerminalBaseChart(_TerminalContent):
    """Association of a base chart with a terminal."""

    class Meta:
        table_name = 'terminal_base_chart'

    base_chart = ForeignKeyField(
        BaseChart, column_name='base_chart', on_delete='CASCADE')
    index = IntegerField(default=0)

    @property
    def chart(self):
        """Returns the respective chart."""
        return self.base_chart.chart

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {
            'id': self.id,
            'chart': self.chart.to_json(mode=ChartMode.BRIEF),
            'index': self.index}


class TerminalConfiguration(_TerminalContent):
    """Association of a configuration with a terminal."""

    class Meta:
        table_name = 'terminal_configuration'

    configuration = ForeignKeyField(
        Configuration, column_name='configuration', on_delete='CASCADE')

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {'id': self.id, 'configuration': self.configuration_id}


class TerminalMenu(_TerminalContent):
    """Association of a menu with a terminal."""

    class Meta:
        table_name = 'terminal_menu'

    menu = ForeignKeyField(Menu, column_name='menu', on_delete='CASCADE')

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {'id': self.id, 'menu': self.menu_id}


MODELS = (TerminalBaseChart, TerminalConfiguration, TerminalMenu)
