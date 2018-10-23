"""Menu tree utilities."""

from collections import defaultdict


__all__ = ['add', 'merge', 'MenuTreeItem']


def add(children):
    """Adds children."""

    child, *children = children

    if not children:
        return child

    for other in children:
        child += other

    return child


def merge(*children_lists):
    """Merges lists of children by name."""

    mapping = defaultdict(list)

    for children in children_lists:
        for child in children:
            mapping[child.name].append(child)

    return [add(children) for children in mapping.values()]


def key(menu_item):
    """Key function for sorting."""

    return menu_item.index


class MenuTreeItem:
    """Menu item for tree structure."""

    __slots__ = (
        'name', 'icon', 'text_color', 'background_color', 'index', 'children')

    def __init__(self, name, icon, text_color, background_color, index,
                 children):
        """Sets the referenced menu item."""
        self.name = name
        self.icon = icon
        self.text_color = text_color
        self.background_color = background_color
        self.index = index
        self.children = children

    @classmethod
    def from_menu_item(cls, menu_item):
        """Creates a menu item tree from the given menu item."""
        children = [
            cls.from_menu_item(child) for child in menu_item.children]
        return cls(
            menu_item.name, menu_item.icon, menu_item.text_color,
            menu_item.background_color, menu_item.index, children=children)

    @classmethod
    def from_menu(cls, menu):
        """Yields menu tree items from the respective menu."""
        return [cls.from_menu_item(menu_item) for menu_item in menu.root_items]

    def __add__(self, other):
        """Adds two menu tree items."""
        if self.name != other.name:
            raise ValueError('Can only add menu items of same name.')

        children = merge(self.children, other.children)
        return type(self)(
            self.name, self.icon, self.text_color, self.background_color,
            self.index, children)
