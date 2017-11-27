"""Terminal content management."""

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

    @property
    def terminal(self):
        """Returns the respective terminal."""
        try:
            return Terminal.get(
                (Terminal.tid == self.vars['tid'])
                & (Terminal.customer == self.customer))
        except DoesNotExist:
            raise NoSuchTerminal() from None

    @property
    def base_charts(self):
        """Yields respective associated with the respective terminal."""
        for record in TerminalBaseChart.select().where(
                TerminalBaseChart.terminal == self.terminal):
            yield record.base_chart

    @property
    def configurations(self):
        """Yields configurations associated with the respective terminal."""
        for record in TerminalConfiguration.select().where(
                TerminalConfiguration.terminal == self.terminal):
            yield record.configuration

    @property
    def menus(self):
        """Yields menus associated with the respective terminal."""
        for record in TerminalMenu.select().where(
                TerminalMenu.group == self.group):
            yield record.menu

    @property
    def tickers(self):
        """Yields tickers associated with the respective terminal."""
        for record in TerminalTicker.select().where(
                TerminalTicker.group == self.group):
            yield record.ticker

    def add_base_chart(self):
        """Adds a new base chart."""
        record = TerminalBaseChart()
        record.terminal = self.terminal
        record.base_chart = self.base_chart

        try:
            record.save()
        except IntegrityError:
            return NoSuchBaseChart()

        return BaseChartAdded()

    def add_configuration(self):
        """Adds the respective configuration."""
        record = TerminalConfiguration()
        record.terminal = self.terminal
        record.configuration = self.self.configuration

        try:
            record.save()
        except IntegrityError:
            return NoSuchConfiguration()

        return ConfigurationAdded()

    def add_menu(self):
        """Adds a new menu."""
        record = TerminalMenu()
        record.terminal = self.terminal
        record.menu = self.menu

        try:
            record.save()
        except IntegrityError:
            return NoSuchMenu()

        return MenuAdded()

    def add_ticker(self):
        """Adds a new menu to the group."""
        record = TerminalTicker()
        record.terminal = self.terminal
        record.ticker = self.ticker

        try:
            record.save()
        except IntegrityError:
            return NoSuchTicker()

        return TickerAdded()

    def delete_base_chart(self):
        """Deletes the respective base chart from the terminal."""
        for record in TerminalBaseChart.select().where(
                (TerminalBaseChart.terminal == self.terminal)
                & (TerminalBaseChart.base_chart == self.content_id)):
            record.delete_instance()

        return BaseChartDeleted()

    def delete_configuration(self):
        """Deletes the respective configuration from the terminal."""
        for record in TerminalConfiguration.select().where(
                (TerminalConfiguration.terminal == self.terminal)
                & (TerminalConfiguration.configuration == self.content_id)):
            record.delete_instance()

        return ConfigurationDeleted()

    def delete_menu(self):
        """Deletes the respective menu from the terminal."""
        for record in TerminalMenu.select().where(
                (TerminalMenu.terminal == self.terminal)
                & (TerminalMenu.menu == self.content_id)):
            record.delete_instance()

        return MenuDeleted()

    def delete_ticker(self):
        """Deletes the respective menu from the group."""
        for record in TerminalTicker.select().where(
                (TerminalTicker.terminal == self.terminal)
                & (TerminalTicker.ticker == self.content_id)):
            record.delete_instance()

        return TickerDeleted()
