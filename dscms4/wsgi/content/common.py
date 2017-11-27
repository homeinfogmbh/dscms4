"""Terminal content management."""

from peewee import DoesNotExist

from wsgilib import InternalServerError, JSON

from his.api.handlers import service, AuthorizedService

from dscms4.messages.common import InvalidId, NoIdSpecified
from dscms4.messages.content import NoSuchBaseChart, NoSuchConfiguration, \
    NoSuchMenu, NoSuchTicker, NoTypeSpecified, InvalidContentType, \
    ContentAdded, ContentDeleted

from dscms4.orm.charts import BaseChart
from dscms4.orm.configuration import Configuration
from dscms4.orm.exceptions import OrphanedBaseChart, AmbiguousBaseChart
from dscms4.orm.menu import Menu
from dscms4.orm.ticker import Ticker
from dscms4.orm.util import chart_of

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

    BASE_CHART = NotImplemented
    CONFIGURATION = NotImplemented
    MENU = NotImplemented
    TICKER = NotImplemented

    @property
    def content_id(self):
        """Returns the identifier of the respective content."""
        try:
            return int(self.data.text)
        except TypeError:
            raise NoIdSpecified() from None
        except ValueError:
            raise InvalidId() from None

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

    @property
    def container(self):
        """Returns the respective container."""
        raise NotImplementedError()

    @property
    def base_charts(self):
        """Yields respective associated with the respective container."""
        for record in self.BASE_CHART.select().where(
                self.BASE_CHART.container == self.container):
            yield record.content

    @property
    def configurations(self):
        """Yields configurations associated with the respective container."""
        for record in self.CONFIGURATION.select().where(
                self.CONFIGURATION.container == self.container):
            yield record.content

    @property
    def menus(self):
        """Yields menus associated with the respective container."""
        for record in self.MENU.select().where(
                self.MENU.container == self.container):
            yield record.content

    @property
    def tickers(self):
        """Yields tickers associated with the respective container."""
        for record in self.TICKER.select().where(
                self.TICKER.container == self.container):
            yield record.ticker

    def add(self, mapping, content):
        """Adds a new content to the container."""
        record = mapping()
        record.container = self.container
        record.content = content
        record.save()
        return ContentAdded()

    def delete_base_chart(self, mapping):
        """Deletes the respective base chart from the container."""
        for record in mapping.select().where(
                (mapping.container == self.container)
                & (mapping.content == self.content_id)):
            record.delete_instance()

        return ContentDeleted()

    def get(self):
        """Lists the content associated with the respective container."""
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
        """Adds new content to the respective container."""
        if self.vars['type'] is None:
            raise NoTypeSpecified() from None
        elif self.vars['type'] == 'chart':
            return self.add(self.BASE_CHART, self.base_chart)
        elif self.vars['type'] == 'configuration':
            return self.add(self.CONFIGURATION, self.configuration)
        elif self.vars['type'] == 'menu':
            return self.add(self.MENU, self.menu)
        elif self.vars['type'] == 'ticker':
            return self.add(self.TICKER, self.ticker)

        raise InvalidContentType() from None

    def delete(self):
        """Deletes content from the respective container."""
        if self.vars['type'] is None:
            raise NoTypeSpecified() from None
        elif self.vars['type'] == 'chart':
            return self.delete(self.BASE_CHART)
        elif self.vars['type'] == 'configuration':
            return self.delete(self.CONFIGURATION)
        elif self.vars['type'] == 'menu':
            return self.delete(self.MENU)
        elif self.vars['type'] == 'ticker':
            return self.delete(self.TICKER)

        raise InvalidContentType() from None
