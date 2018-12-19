"""Common functions."""

from contextlib import suppress
from functools import partial
from itertools import chain
from logging import getLogger

from functoolsplus import cached_method, coerce     # pylint: disable=E0401

from dscms4 import dom  # pylint: disable=E0611
from dscms4.exceptions import AmbiguousBaseChart
from dscms4.exceptions import OrphanedBaseChart
from dscms4.menutree import merge, MenuTreeItem
from dscms4.orm.charts import BaseChart, ChartMode
from dscms4.orm.configuration import Configuration
from dscms4.orm.content.group import GroupConfiguration
from dscms4.orm.menu import MenuItem, MenuItemChart


__all__ = ['charts', 'identify', 'indexify', 'level_configs', 'uniquesort']


LOGGER = getLogger(__file__)


@coerce(tuple)
def charts(base_charts):
    """Yields the charts of the respective base charts."""

    for base_chart in base_charts:
        try:
            yield base_chart.chart
        except OrphanedBaseChart:
            LOGGER.error('Base chart is orphaned: %s.', base_chart)
        except AmbiguousBaseChart:
            LOGGER.error('Base chart is ambiguous: %s.', base_chart)


def identify(item):
    """Returns the item's ID."""

    return item.id


def indexify(item):
    """Returns the item's index."""

    return item.index


@coerce(frozenset)
def level_configs(level):
    """Yields all configurations of a certain group level."""

    return Configuration.select().join(GroupConfiguration).where(
        GroupConfiguration.group << level)


def uniquesort(iterable, *, key=None, reverse=False):
    """Uniquely sorts an iterable."""

    return sorted(frozenset(iterable), key=key, reverse=reverse)


class PresentationMixin:
    """Common presentation mixin."""

    @property
    @cached_method()
    @coerce(charts)
    def menu_charts(self):
        """Yields charts of the terminal's menu."""
        yield from BaseChart.select().join(MenuItemChart).join(MenuItem).where(
            (BaseChart.trashed == 0) & (MenuItem.menu << self.menus))

    @property
    def menutree(self):
        """Returns the merged menu tree."""
        items = chain(*(MenuTreeItem.from_menu(menu) for menu in self.menus))
        return sorted(merge(items), key=indexify)

    @property
    @coerce(partial(uniquesort, key=identify))
    def charts(self):
        """Yields all charts for this terminal."""
        yield from self.playlist
        yield from self.menu_charts

    @property
    @cached_method()
    @coerce(frozenset)
    def files(self):
        """Yields the presentation's used file IDs."""
        yield from self.configuration.files

        for chart in self.charts:
            try:
                files = chart.files
            except AttributeError:
                continue

            yield from files

    def to_dom(self):
        """Returns an XML dom presentation."""
        xml = dom.presentation()
        xml.customer = self.customer.id

        with suppress(AttributeError):
            xml.tid = self.terminal.tid

        xml.configuration = self.configuration.to_dom()
        xml.playlist = [chart.to_dom(brief=True) for chart in self.playlist]
        xml.menu_item = [item.to_dom() for item in self.menutree]
        xml.chart = [chart.to_dom() for chart in self.charts]
        return xml

    def to_json(self):
        """Returns a JSON presentation."""
        json = {
            'customer': self.customer.id,
            'configuration': self.configuration.to_json(cascade=True),
            'playlist': [
                chart.to_json(mode=ChartMode.BRIEF)
                for chart in self.playlist],
            'menuItems': [item.to_json() for item in self.menutree],
            'charts': [chart.to_json() for chart in self.charts]}

        with suppress(AttributeError):
            json['tid'] = self.terminal.tid

        return json
