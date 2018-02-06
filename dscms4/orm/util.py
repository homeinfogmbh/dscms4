"""ORM utility functions."""

from collections import namedtuple
from sys import stderr

from dscms4.orm import charts, content, chart_types, configuration, group, \
    menu, schedule, tags, ticker
from dscms4.orm.charts.common import BaseChart
from dscms4.orm.exceptions import OrphanedBaseChart, AmbiguousBaseChart


__all__ = ['create_tables', 'charts_of', 'chart_of', 'check_base_charts']


MODELS = (
    charts.MODELS + content.MODELS + chart_types.MODELS + configuration.MODELS
    + group.MODELS + menu.MODELS + schedule.MODELS + tags.MODELS
    + ticker.MODELS)
CheckResult = namedtuple('CheckResult', ('orphans', 'ambiguous'))


def create_tables(*args, **kwargs):
    """Creates the respective database tables."""

    for model in MODELS:
        model.create_table(*args, **kwargs)


def charts_of(base_chart):
    """Yields all charts that associate this base chart."""

    for cls in charts.CHARTS.values():
        for chart in cls.select().where(cls.base_chart == base_chart):
            yield chart


def chart_of(base_chart):
    """Returns the mapped implementation of the respective base chart."""

    try:
        match, *superfluous = charts_of(base_chart)
    except ValueError:
        raise OrphanedBaseChart(base_chart)

    if superfluous:
        raise AmbiguousBaseChart(base_chart, [match] + superfluous)

    return match


def check_base_charts(verbose=False):
    """Checks base charts."""

    orphans = []
    ambiguous = []

    for base_chart in BaseChart:
        try:
            chart = chart_of(base_chart)
        except OrphanedBaseChart as orphaned_base_chart:
            orphans.append(base_chart)

            if verbose:
                print(orphaned_base_chart, file=stderr)
        except AmbiguousBaseChart as ambiguous_base_chart:
            ambiguous.append(base_chart)

            if verbose:
                print(ambiguous_base_chart, file=stderr)
        else:
            if verbose:
                print(base_chart, '↔', chart)

    return CheckResult(orphans, ambiguous)
