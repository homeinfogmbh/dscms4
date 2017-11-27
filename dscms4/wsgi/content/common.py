"""Terminal content management."""

from terminallib import Terminal
from wsgilib import routed

from his.api.handlers import service, AuthorizedService

from dscms4.orm.charts import BaseChart
from dscms4.orm.configuration import Configuration
from dscms4.orm.menu import Menu
from dscms4.orm.ticker import Ticker

__all__ = ['ContentHandler']


def json_with_hint(base_chart):
    """Returns a JSON-ish respresentation
    of the base chart with a type hint.
    """

    dictionary = base_chart.to_dict()

    try:
        chart = chart_of(base_chart)
    except (OrphanedBaseChart, AmbiguousBaseChart) as error:
        raise InternalServerError(str(error)) from None

    dictionary['type'] = chart.__class__.__name__
    return dictionary


@service('dscms4')
class ContentHandler(AuthorizedService):
    """Handles content associated with terminals."""

    @property
    def content_id(self):
        """Returns the identifier of the respective content."""
        try:
            return int(self.data.text)
        except TypeError:
            raise NoIDSpecified() from None
        except ValueError:
            raise NotAnInteger() from None

    @property
    def base_chart(self):
        """Returns the respective base chart."""
        try:
            return BaseChart.get(
                (BaseChart.id == self.content_id)
                & (BaseChart.customer == self.customer))
        except DoesNotExist:
            raise NoSuchBaseChart() from None

    @property
    def configuration(self):
        """Returns the respective configuration."""
        try:
            return Configuration.get(
                (Configuration.id == self.content_id)
                & (Configuration.customer == self.customer))
        except DoesNotExist:
            raise NoSuchConfiguration() from None

    @property
    def menu(self):
        """Returns the respective menu."""
        try:
            return Menu.get(
                (Menu.id == self.content_id)
                & (Menu.customer == self.customer))
        except DoesNotExist:
            raise NoSuchMenu() from None

    @property
    def ticker(self):
        """Returns the respective ticker."""
        try:
            return Ticker.get(
                (Ticker.id == self.content_id)
                & (Ticker.customer == self.customer))
        except DoesNotExist:
            raise NoSuchTicker() from None

    @property
    def accumulated_content(self):
        """Returns the accumulated content."""
        return {
            'charts': [json_with_hint(chart) for chart in self.base_charts],
            'configurations': [cfg.to_dict() for cfg in self.configurations],
            'menus': [menu.to_dict() for menu in self.menus],
            'tickers': [ticker.to_dict() for ticker in self.tickers]}

    def get(self):
        """Lists the content associated with the respective group."""
        if self.vars['type'] is None:
            return JSON(self.accumulated_content)
        elif self.vars['type'] == 'chart':
            return JSON([json_with_hint(chart) for chart in self.base_charts])
        elif self.vars['type'] == 'configuration':
            return JSON([config.to_dict() for config in self.configurations])
        elif self.vars['type'] == 'menu':
            return JSON([menu.to_dict() for menu in self.menus])
        elif self.vars['type'] == 'ticker':
            return JSON([ticker.to_dict() for ticker in self.tickers])

        raise InvalidContentType() from None

    def post(self):
        """Adds new content to the respective group."""
        if self.vars['type'] is None:
            raise NoTypeSpecified() from None
        elif self.vars['type'] == 'chart':
            return self.add_base_chart()
        elif self.vars['type'] == 'configuration':
            return self.add_configuration()
        elif self.vars['type'] == 'menu':
            return self.add_menu()
        elif self.vars['type'] == 'ticker':
            return self.add_ticker()

        raise InvalidContentType() from None

    def delete(self):
        """Deletes content from the respective group."""
        if self.vars['type'] is None:
            raise NoTypeSpecified() from None
        elif self.vars['type'] == 'chart':
            return self.delete_base_chart()
        elif self.vars['type'] == 'configuration':
            return self.delete_configuration()
        elif self.vars['type'] == 'menu':
            return self.delete_menu()
        elif self.vars['type'] == 'ticker':
            return self.delete_ticker()

        raise InvalidContentType() from None
