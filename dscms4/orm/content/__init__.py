"""Content mappings.

This package provides modules to map
content on so-called "clients".
"""
from dscms4.orm.content.comcat_account import ComCatAccountBaseChart, \
    ComCatAccountConfiguration, ComCatAccountMenu, ComCatAccountTicker
from dscms4.orm.content.group import GroupBaseChart, GroupConfiguration, \
    GroupMenu, GroupTicker
from dscms4.orm.content.terminal import TerminalBaseChart, \
    TerminalConfiguration, TerminalMenu, TerminalTicker

__all__ = [
    'ComCatAccountBaseChart',
    'ComCatAccountConfiguration',
    'ComCatAccountMenu',
    'ComCatAccountTicker',
    'GroupBaseChart',
    'GroupConfiguration',
    'GroupMenu',
    'GroupTicker',
    'TerminalBaseChart',
    'TerminalConfiguration',
    'TerminalMenu',
    'TerminalTicker']
