"""Async stuff."""

from asyncio import coroutine, get_event_loop, sleep, wait

from peeweeplus.query import async_lists

from dscms4.orm.content.terminal import TerminalBaseChart
from dscms4.orm.content.terminal import TerminalConfiguration
from dscms4.orm.content.terminal import TerminalMenu


__all__ = ['async_dict', 'async_json']


@coroutine
def _async_conv(item, keyfunc, valfunc):
    """Async dict generator."""

    value = valfunc(item)
    yield from sleep(0)
    return (keyfunc(item), value)


@coroutine
def _async_dict(iterable, keyfunc, valfunc):
    """Async dict generator."""

    tasks = []

    for item in iterable:
        task = _async_conv(item, keyfunc, valfunc)
        tasks.append(task)

    return wait(tasks)


def async_dict(iterable, keyfunc, valfunc=lambda item: item):
    """Performs select queries in parallel."""

    loop = get_event_loop()
    coro = _async_dict(iterable, keyfunc, valfunc)
    tasks, _ = loop.run_until_complete(coro)
    return dict(task.result() for task in tasks)


def async_json(iterable, keyfunc=lambda item: item.id,
               valfunc=lambda item: item.to_json()):
    """Converts an iterable into a JSON-ish dict."""

    return async_dict(iterable, keyfunc, valfunc)


def async_terminals_json(terminals):
    """Async JSON conversion."""

    return async_json(
        terminals,
        valfunc=lambda terminal: TerminalContent(terminal).to_json())


class TerminalContent:
    """Represents content of a terminal."""

    def __init__(self, terminal):
        """Sets the terminal."""
        self.terminal = terminal

    @property
    def charts(self):
        """Yields the terminal's charts."""
        for terminal_base_chart in TerminalBaseChart.select().where(
                TerminalBaseChart.terminal == self.terminal):
            yield terminal_base_chart.to_json()

    @property
    def configurations(self):
        """Yields the terminal's configurations."""
        for terminal_configuration in TerminalConfiguration.select().where(
                TerminalConfiguration.terminal == self.terminal):
            yield terminal_configuration.to_json()

    @property
    def menus(self):
        """Yields the terminal's menus."""
        for terminal_menu in TerminalMenu.select().where(
                TerminalMenu.terminal == self.terminal):
            yield terminal_menu.to_json()

    def to_json(self):
        """Returns content."""
        address = self.terminal.address
        yield ('address', address.to_json())
        yield from async_lists(
            charts=self.charts, configurations=self.configurations,
            menus=self.menus)
