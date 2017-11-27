"""Group content management."""

from wsgilib import routed

from his.api.handlers import service, AuthorizedService

from dscms4.orm.content.group import GroupBaseChart, GroupConfiguration, \
    GroupMenu, GroupTicker
from dscms4.orm.group import Group

from .common import ContentHandler

__all__ = ['GroupContent']


@routed('/content/group/<id:int>/[type]')
class GroupContent(ContentHandler):
    """Handles content associated with groups."""

    @property
    def group(self):
        """Returns the respective group."""
        try:
            return Group.get(
                (Group.id == self.vars['id'])
                & (Group.customer == self.customer))
        except DoesNotExist:
            raise NoSuchGroup() from None

    @property
    def base_charts(self):
        """Yields respective associated with the respective group."""
        for record in GroupBaseChart.select().where(
                GroupBaseChart.group == self.group):
            yield record.base_chart

    @property
    def configurations(self):
        """Yields configurations associated with the respective group."""
        for record in GroupConfiguration.select().where(
                GroupConfiguration.group == self.group):
            yield record.configuration

    @property
    def menus(self):
        """Yields menus associated with the respective group."""
        for record in GroupMenu.select().where(GroupMenu.group == self.group):
            yield record.menu

    @property
    def tickers(self):
        """Yields tickers associated with the respective group."""
        for record in GroupTicker.select().where(
                GroupTicker.group == self.group):
            yield record.ticker

    def add_base_chart(self):
        """Adds a new base chart."""
        record = GroupBaseChart()
        record.group = self.group
        record.base_chart = self.base_chart

        try:
            record.save()
        except IntegrityError:
            return NoSuchBaseChart()

        return BaseChartAdded()

    def add_configuration(self):
        """Adds the respective configuration."""
        record = GroupConfiguration()
        record.group = self.group
        record.configuration = self.self.configuration

        try:
            record.save()
        except IntegrityError:
            return NoSuchConfiguration()

        return ConfigurationAdded()

    def add_menu(self):
        """Adds a new menu to the group."""
        record = GroupMenu()
        record.group = self.group
        record.menu = self.menu

        try:
            record.save()
        except IntegrityError:
            return NoSuchMenu()

        return MenuAdded()

    def add_ticker(self):
        """Adds a new menu to the group."""
        record = GroupTicker()
        record.group = self.group
        record.ticker = self.ticker

        try:
            record.save()
        except IntegrityError:
            return NoSuchTicker()

        return TickerAdded()

    def delete_base_chart(self):
        """Deletes the respective base chart from the group."""
        for record in GroupBaseChart.select().where(
                (GroupBaseChart.group == self.group)
                & (GroupBaseChart.base_chart == self.content_id)):
            record.delete_instance()

        return BaseChartDeleted()

    def delete_configuration(self):
        """Deletes the respective configuration from the group."""
        for record in GroupConfiguration.select().where(
                (GroupConfiguration.group == self.group)
                & (GroupConfiguration.configuration == self.content_id)):
            record.delete_instance()

        return ConfigurationDeleted()

    def delete_menu(self):
        """Deletes the respective menu from the group."""
        for record in GroupMenu.select().where(
                (GroupMenu.group == self.group)
                & (GroupMenu.menu == self.content_id)):
            record.delete_instance()

        return MenuDeleted()

    def delete_ticker(self):
        """Deletes the respective menu from the group."""
        for record in GroupTicker.select().where(
                (GroupTicker.group == self.group)
                & (GroupTicker.ticker == self.content_id)):
            record.delete_instance()

        return TickerDeleted()
