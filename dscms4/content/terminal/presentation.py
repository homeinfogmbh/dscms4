"""Terminal presentation."""

from contextlib import suppress

from dscms4 import dom
from dscms4.content.terminal.charts import accumulated_charts
from dscms4.content.terminal.configuration import first_configuration
from dscms4.content.terminal.menu import accumulated_menus

__all__ = ['Presentation']


class Presentation:
    """Represents presentation data for a terminal."""

    def __init__(self, terminal):
        """Sets the respective terminal."""
        self.terminal = terminal

    @property
    def tid(self):
        """Returns the terminal ID."""
        return self.terminal.tid

    @property
    def cid(self):
        """Returns the customer ID."""
        return self.terminal.customer.id

    @property
    def configuration(self):
        """Returns the respective configuration."""
        return first_configuration(self.terminal)

    @property
    def charts(self):
        """Yields the terminal's charts."""
        return accumulated_charts(self.terminal)

    @property
    def menus(self):
        """Yields the terminal's menus."""
        return accumulated_menus(self.terminal)

    @property
    def files(self):
        """Yields the presentation's used file IDs."""
        files = set(self.configuration.files)

        for _, chart in self.charts:
            with suppress(AttributeError):
                files |= chart.files

        return files

    def to_dom(self):
        """Returns an XML dom presentation."""
        xml = dom.presentation()
        xml.customer = self.cid
        xml.tid = self.tid
        xml.configuration = self.configuration.to_dom()
        xml.chart = [chart.to_dom() for _, chart in self.charts]
        xml.menu = [menu.to_dom() for _, menu in self.menus]
        return xml

    def to_dict(self):
        """Returns a JSON presentation."""
        return {
            'customer': self.cid,
            'tid': self.tid,
            'configuration': self.configuration.to_dict(),
            'charts': [chart.to_dict() for _, chart in self.charts],
            'menus': [menu.to_dict() for _, menu in self.menus]}
