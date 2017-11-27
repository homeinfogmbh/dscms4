"""ComCat account content management."""

from wsgilib import routed

from his.api.handlers import service, AuthorizedService

from dscms4.orm.content.comcat_account import ComCatAccountBaseChart, \
    ComCatAccountConfiguration, ComCatAccountMenu, ComCatAccountTicker
from dscms4.orm.group import Group

from .common import ContentHandler

__all__ = ['ComCatAccountContent']


@routed('/content/group/<id:int>/[type]')
class ComCatAccountContent(ContentHandler):
    """Handles content associated with ComCat accounts."""

    @property
    def comcat_account(self):
        """Returns the respective ComCat account."""
        try:
            return ComCatAccount.get(
                (ComCatAccount.id == self.vars['id'])
                & (ComCatAccount.customer == self.customer))
        except DoesNotExist:
            raise NoSuchGroup() from None

    @property
    def base_charts(self):
        """Yields respective associated with the respective ComCat account."""
        for record in ComCatAccountBaseChart.select().where(
                ComCatAccountBaseChart.comcat_account == self.comcat_account):
            yield record.base_chart

    @property
    def configurations(self):
        """Yields configurations associated
        with the respective ComCat account.
        """
        for record in ComCatAccountConfiguration.select().where(
                ComCatAccountConfiguration.comcat_account
                == self.comcat_account):
            yield record.configuration

    @property
    def menus(self):
        """Yields menus associated with the respective ComCat account."""
        for record in ComCatAccountMenu.select().where(
                ComCatAccountMenu.comcat_account == self.comcat_account):
            yield record.menu

    @property
    def tickers(self):
        """Yields tickers associated with the respective ComCat account."""
        for record in ComCatAccountTicker.select().where(
                ComCatAccountTicker.comcat_account == self.comcat_account):
            yield record.ticker

    def add_base_chart(self):
        """Adds a new base chart."""
        record = ComCatAccountBaseChart()
        record.comcat_account = self.comcat_account
        record.base_chart = self.base_chart

        try:
            record.save()
        except IntegrityError:
            return NoSuchBaseChart()

        return BaseChartAdded()

    def add_configuration(self):
        """Adds the respective configuration."""
        record = ComCatAccountConfiguration()
        record.comcat_account = self.comcat_account
        record.configuration = self.self.configuration

        try:
            record.save()
        except IntegrityError:
            return NoSuchConfiguration()

        return ConfigurationAdded()

    def add_menu(self):
        """Adds a new menu to the ComCat account."""
        record = ComCatAccountMenu()
        record.comcat_account = self.comcat_account
        record.menu = self.menu

        try:
            record.save()
        except IntegrityError:
            return NoSuchMenu()

        return MenuAdded()

    def add_ticker(self):
        """Adds a new menu to the ComCat account."""
        record = ComCatAccountTicker()
        record.comcat_account = self.comcat_account
        record.ticker = self.ticker

        try:
            record.save()
        except IntegrityError:
            return NoSuchTicker()

        return TickerAdded()

    def delete_base_chart(self):
        """Deletes the respective base chart from the ComCat account."""
        for record in ComCatAccountBaseChart.select().where(
                (ComCatAccountBaseChart.comcat_account == self.comcat_account)
                & (ComCatAccountBaseChart.base_chart == self.content_id)):
            record.delete_instance()

        return BaseChartDeleted()

    def delete_configuration(self):
        """Deletes the respective configuration from the ComCat account."""
        for record in ComCatAccountConfiguration.select().where(
                (ComCatAccountConfiguration.comcat_account
                 == self.comcat_account)
                & (ComCatAccountConfiguration.configuration
                == self.content_id)):
            record.delete_instance()

        return ConfigurationDeleted()

    def delete_menu(self):
        """Deletes the respective menu from the ComCat account."""
        for record in ComCatAccountMenu.select().where(
                (ComCatAccountMenu.comcat_account == self.comcat_account)
                & (ComCatAccountMenu.menu == self.content_id)):
            record.delete_instance()

        return MenuDeleted()

    def delete_ticker(self):
        """Deletes the respective menu from the ComCat account."""
        for record in ComCatAccountTicker.select().where(
                (ComCatAccountTicker.comcat_account == self.comcat_account)
                & (ComCatAccountTicker.ticker == self.content_id)):
            record.delete_instance()

        return TickerDeleted()
