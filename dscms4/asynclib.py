"""Async stuff."""

from asyncio import coroutine, get_event_loop, sleep, wait


__all__ = ['async_dict']


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


def async_dict(iterable, keyfunc, valfunc):
    """Performs select queries in parallel."""

    loop = get_event_loop()
    coro = _async_dict(iterable, keyfunc, valfunc)
    tasks, _ = loop.run_until_complete(coro)
    return dict(task.result() for task in tasks)
