"""Menu tree utilities."""

from collections import defaultdict
from itertools import chain
from json import dumps

from dscms4 import dom


__all__ = ['add', 'merge', 'get_index', 'MenuTreeItem']


def add(children):
    """Adds children."""

    child, *children = children

    if not children:
        return child

    for other in children:
        child += other

    return child


def merge(children):
    """Merges lists of children by name."""

    mapping = defaultdict(list)

    for child in children:
        mapping[child.signature].append(child)

    return [add(children) for children in mapping.values()]


def get_index(menu_item):
    """Key function for sorting."""

    return menu_item.index


class MenuTreeItem:
    """Menu item for tree structure."""

    __slots__ = (
        'name', 'icon', 'text_color', 'background_color', 'index',
        'menu_item_charts', 'children')

    def __init__(self, name, icon, text_color, background_color, index,
                 menu_item_charts, children):
        """Sets the referenced menu item."""
        self.name = name
        self.icon = icon
        self.text_color = text_color
        self.background_color = background_color
        self.index = index
        self.menu_item_charts = menu_item_charts
        self.children = children

    def __str__(self):
        """Returns a nested JSON object."""
        return dumps(self.to_json(), indent=2)

    def __add__(self, other):
        """Adds two menu tree items."""
        if self.signature != other.signature:
            raise ValueError('Can only add menu items with same signature.')

        children = merge(chain(self.children, other.children))
        base_charts = set()
        menu_item_charts = set()

        for mic in chain(self.menu_item_charts, other.menu_item_charts):
            if mic.base_chart_id not in base_charts:
                base_charts.add(mic.base_chart_id)
                menu_item_charts.add(mic)

        return type(self)(
            self.name, self.icon, self.text_color, self.background_color,
            self.index, menu_item_charts, children)

    @classmethod
    def from_menu_item(cls, menu_item):
        """Creates a menu item tree from the given menu item."""
        children = [
            cls.from_menu_item(child) for child in menu_item.children]
        menu_item_charts = list(menu_item.menu_item_charts)
        return cls(
            menu_item.name, menu_item.icon, menu_item.text_color,
            menu_item.background_color, menu_item.index, menu_item_charts,
            children)

    @classmethod
    def from_menu(cls, menu):
        """Yields menu tree items from the respective menu."""
        return [cls.from_menu_item(menu_item) for menu_item in menu.root_items]

    @property
    def signature(self):
        """Returns a tuple, identifying the menu tree item."""
        return (self.name, self.icon, self.text_color, self.background_color)

    def to_json(self):
        """Returns a nested JSON-ish dict."""
        return {
            'name': self.name,
            'icon': self.icon,
            'textColor': self.text_color,
            'backgroundColor': self.background_color,
            'index': self.index,
            'charts': [
                menu_item_chart.to_json() for menu_item_chart
                in sorted(self.menu_item_charts, key=get_index)
                if not menu_item_chart.base_chart.trashed],
            'menuItems': [
                child.to_json() for child in sorted(
                    self.children, key=get_index)]}

    def to_dom(self):
        """Returns an XML DOM of the model."""
        xml = dom.MenuItem()
        xml.name = self.name
        xml.icon = self.icon
        xml.text_color = self.text_color
        xml.background_color = self.background_color
        xml.index = self.index
        xml.menu_item = [item.to_dom() for item in self.children]
        xml.chart = [
            menu_item_chart.to_dom() for menu_item_chart
            in sorted(self.menu_item_charts, key=get_index)
            if not menu_item_chart.base_chart.trashed]
        return xml
