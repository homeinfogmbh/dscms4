"""ORM utility functions."""

from collections import namedtuple
from sys import stderr

from dscms4.exceptions import OrphanedBaseChart, AmbiguousBaseChart
from dscms4.orm.charts import CHARTS
from dscms4.orm.charts.common import BaseChart


__all__ = ['charts_of', 'chart_of', 'check_base_charts']


CheckResult = namedtuple('CheckResult', ('orphans', 'ambiguous'))


def charts_of(base_chart):
    """Yields all charts that associate this base chart."""

    for cls in CHARTS.values():
        for chart in cls.select().where(cls.base == base_chart):
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

    orphans = set()
    ambiguous = set()

    for base_chart in BaseChart:
        try:
            chart = chart_of(base_chart)
        except OrphanedBaseChart as orphaned_base_chart:
            orphans.add(base_chart)

            if verbose:
                print(orphaned_base_chart, file=stderr)
        except AmbiguousBaseChart as ambiguous_base_chart:
            ambiguous.add(base_chart)

            if verbose:
                print(ambiguous_base_chart, file=stderr)
        else:
            if verbose:
                print(base_chart, '↔', chart)

    return CheckResult(frozenset(orphans), frozenset(ambiguous))
