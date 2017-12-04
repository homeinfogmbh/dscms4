"""Object relatinal mappings.

This package provides the CMS's database models.
"""

from dscms4.orm.charts import BaseChart, Facebook, Account, GuessPicture, \
    ImageText, Image, Text, News, PublicTransport, Quotes, Video, Weather
from dscms4.orm.content import ComCatAccountBaseChart, \
    ComCatAccountConfiguration, ComCatAccountMenu, ComCatAccountTicker, \
    GroupBaseChart, GroupConfiguration, GroupMenu, GroupTicker, \
    TerminalBaseChart, TerminalConfiguration, TerminalMenu, TerminalTicker
from dscms4.orm.configuration import Colors, Configuration, Backlight
from dscms4.orm.group import Group, GroupMemberTerminal, \
    GroupMemberComCatAccount, GroupMemberApartmentBuilding
from dscms4.orm.menu import Menu, MenuItem
from dscms4.orm.ticker import Ticker, TickerText, TickerURL, \
    TickerTextMapping, TickerURLMapping


MODELS = [
    BaseChart, Facebook, Account, GuessPicture, ImageText, Image, Text, News,
    PublicTransport, Quotes, Video, Weather, ComCatAccountBaseChart,
    ComCatAccountConfiguration, ComCatAccountMenu, ComCatAccountTicker,
    GroupBaseChart, GroupConfiguration, GroupMenu, GroupTicker,
    TerminalBaseChart, TerminalConfiguration, TerminalMenu, TerminalTicker,
    Colors, Configuration, Backlight, Group, GroupMemberTerminal,
    GroupMemberComCatAccount, GroupMemberApartmentBuilding, Menu, MenuItem,
    Ticker, TickerText, TickerURL, TickerTextMapping, TickerURLMapping]


def create_tables(fail_silently=True):
    """Create the respective tables."""

    for model in MODELS:
        try:
            model.create_table(fail_silently=fail_silently)
        except Exception:
            print('Could not create table for model "{}".'.format(model),
                  file=stderr)
