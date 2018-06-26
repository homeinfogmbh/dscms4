"""Terminal presentation."""

from contextlib import suppress
from itertools import chain

from dscms4 import dom
from dscms4.content.terminal.charts import accumulated_charts
from dscms4.content.terminal.configuration import first_configuration
from dscms4.content.terminal.menu import accumulated_menus, \
    accumulated_charts as accumulated_menu_charts

__all__ = ['Presentation']


class Presentation:
    """Represents presentation data for a terminal."""

    def __init__(self, terminal):
        """Sets the respective terminal."""
        self.terminal = terminal

    @property
    def configuration(self):
        """Returns the respective configuration."""
        return first_configuration(self.terminal)

    @property
    def charts(self):
        """Yields the terminal's charts."""
        for _, chart in accumulated_charts(self.terminal):
            yield chart

    @property
    def menus(self):
        """Yields the terminal's menus."""
        for _, menu in accumulated_menus(self.terminal):
            yield menu

    def file_set(self, configuration=None, chart_set=None, charts=None):
        """Yields the presentation's used file IDs."""
        if configuration is None:
            configuration = self.configuration

        if chart_set is None:
            chart_set = self.chart_set(charts=charts)

        files = configuration.files

        for chart in chart_set:
            with suppress(AttributeError):
                files |= chart.files

        return files

    def menu_charts(self, menus=None):
        """Yields accumulated charts from menus."""
        if menus is None:
            menus = self.menus

        for menu in menus:
            for _, chart in accumulated_menu_charts(menu):
                yield chart

    def chart_set(self, charts=None, menu_charts=None, menus=None):
        """Returns a set of unique charts."""
        if charts is None:
            charts = self.charts

        if menu_charts is None:
            menu_charts = self.menu_charts(menus=menus)

        return set(chain(charts, menu_charts))

    def to_dom(self):
        """Returns an XML dom presentation."""
        xml = dom.presentation()
        xml.customer = self.terminal.customer.id
        xml.tid = self.terminal.tid
        xml.configuration = self.configuration.to_dom()
        charts = tuple(self.charts)
        xml.playlist = [chart.to_dom(brief=True) for chart in charts]
        menus = tuple(self.menus)
        xml.menu = [menu.to_dom() for menu in menus]
        xml.chart = [
            chart.to_dom() for chart in self.chart_set(
                charts=charts, menus=menus)]
        return xml

    def to_dict(self):
        """Returns a JSON presentation."""
        charts = tuple(self.charts)
        menus = tuple(self.menus)
        return {
            'customer': self.terminal.customer.id,
            'tid': self.terminal.tid,
            'configuration': self.configuration.to_dict(),
            'playlist': [chart.to_dict(brief=True) for chart in charts],
            'menus': [menu.to_dict() for menu in menus],
            'charts': [chart.to_dict() for chart inself.chart_set(
                charts=charts, menus=menus)]}
