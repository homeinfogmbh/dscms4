"""Async stuff."""

from asyncio import coroutine, get_event_loop, sleep, wait
from logging import getLogger


__all__ = ['async_dict']


LOGGER = getLogger(__file__)


@coroutine
def _async_conv(item, keyfunc, valfunc):
    """Async dict generator."""

    value = valfunc(item)
    yield from sleep(0)
    key = keyfunc(item)
    LOGGER.warning('Returning: %s.', key)
    return (key, value)


@coroutine
def _async_conversions(iterable, keyfunc, valfunc):
    """Async dict generator."""

    tasks = []

    for item in iterable:
        task = _async_conv(item, keyfunc, valfunc)
        tasks.append(task)

    yield from tasks


@coroutine
def _async_dict(iterable, keyfunc, valfunc):
    """Async dict generator."""

    tasks = []
    result = {}

    for task in _async_conversions(iterable, keyfunc, valfunc):
        tasks.append(task)
        key, value = task
        result[key] = value

    wait(tasks)
    return result


def async_dict(iterable, keyfunc, valfunc):
    """Performs select queries in parallel."""

    loop = get_event_loop()
    coro = _async_dict(iterable, keyfunc, valfunc)
    tasks, _ = loop.run_until_complete(coro)
    LOGGER.warning('Tasks: %s.', tasks)
    return dict(task.result() for task in tasks)
