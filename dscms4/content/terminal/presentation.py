"""Terminal presentation."""

from contextlib import suppress
from functools import lru_cache
from itertools import chain

from functoolsplus import returning

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
    @lru_cache(maxsize=1)
    def configuration(self):
        """Returns the respective configuration."""
        return first_configuration(self.terminal)

    @property
    @lru_cache(maxsize=1)
    @returning(tuple)
    def charts(self):
        """Yields the terminal's charts."""
        for _, chart in accumulated_charts(self.terminal):
            yield chart

    @property
    @lru_cache(maxsize=1)
    @returning(tuple)
    def menus(self):
        """Yields the terminal's menus."""
        for _, menu in accumulated_menus(self.terminal):
            yield menu

    @property
    @lru_cache(maxsize=1)
    def files(self):
        """Yields the presentation's used file IDs."""
        files = self.configuration.files

        for chart in self.chart_set:
            with suppress(AttributeError):
                files |= chart.files

        return files

    @property
    @lru_cache(maxsize=1)
    @returning(tuple)
    def menu_charts(self):
        """Yields accumulated charts from menus."""
        for menu in self.menus:
            for _, chart in accumulated_menu_charts(menu):
                yield chart

    @property
    @lru_cache(maxsize=1)
    def chart_set(self):
        """Returns a set of unique charts."""
        return set(chain(self.charts, self.menu_charts))

    def to_dom(self):
        """Returns an XML dom presentation."""
        xml = dom.presentation()
        xml.customer = self.terminal.customer.id
        xml.tid = self.terminal.tid
        xml.configuration = self.configuration.to_dom()
        xml.playlist = [chart.to_dom(brief=True) for chart in self.charts]
        xml.menu = [menu.to_dom() for menu in self.menus]
        xml.chart = [chart.to_dom() for chart in self.chart_set]
        return xml

    def to_dict(self):
        """Returns a JSON presentation."""
        return {
            'customer': self.terminal.customer.id,
            'tid': self.terminal.tid,
            'configuration': self.configuration.to_dict(),
            'playlist': [chart.to_dict(brief=True) for chart in self.charts],
            'menus': [menu.to_dict() for menu in self.menus],
            'charts': [chart.to_dict() for chart in self.chart_set]}
