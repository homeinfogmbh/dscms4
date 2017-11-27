"""WSGI service for content management."""

from wsgilib import routed

from his.api.handlers import service, AuthorizedService

from dscms4.orm.content.group import GroupBaseChart, GroupConfiguration, \
    GroupMenu, GroupTicker
from dscms4.orm.group import Group


@service('dscms4')
@routed('/content/group/<id:int>/[type]')
class GroupContent(AuthorizedService):
    """Handles content associated with groups."""

    @property
    def group(self):
        """Returns the respective group."""
        return Group.get(
            (Group.id == self.vars['id']) & (Group.customer == self.customer))

    @property
    def charts(self):
        """Yields respective associated with the respective group."""
        for record in GroupBaseChart.select().where(
                GroupBaseChart.group == self.group):
            yield chart_of(record.base_chart)

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

    @property
    def accumulated_content(self):
        """Returns the accumulated content for the respective group."""
        return {
            'charts': [chart.to_dict() for chart in self.charts],
            'configurations': [cfg.to_dict() for cfg in self.configurations],
            'menus': [menu.to_dict() for menu in self.menus],
            'tickers': [ticker.to_dict() for ticker in self.tickers]}

    def get(self):
        """Lists the content associated with the respective group."""
        if self.vars['type'] is None:
            return JSON(self.accumulated_content)
        elif self.vars['type'] == 'chart':
            return JSON([chart.to_dict() for chart in self.charts])
        elif self.vars['type'] == 'configuration':
            return JSON([config.to_dict() for config in self.configurations])
        elif self.vars['type'] == 'menu':
            return JSON([menu.to_dict() for menu in self.menus])
        elif self.vars['type'] == 'ticker':
            return JSON([ticker.to_dict() for ticker in self.tickers])

        raise InvalidContentType() from None
