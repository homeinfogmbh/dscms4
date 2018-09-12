"""ORM utility functions."""

from collections import namedtuple
from logging import getLogger

from dscms4.exceptions import OrphanedBaseChart, AmbiguousBaseChart
from dscms4.orm.charts import CHARTS
from dscms4.orm.charts.common import BaseChart


__all__ = ['charts_of', 'chart_of', 'check_base_charts']


LOGGER = getLogger('DSCMS4 ORM Utility')


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
        raise AmbiguousBaseChart(base_chart, frozenset([match] + superfluous))

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
                LOGGER.error(orphaned_base_chart)
        except AmbiguousBaseChart as ambiguous_base_chart:
            ambiguous.add(base_chart)

            if verbose:
                LOGGER.error(ambiguous_base_chart)
        else:
            if verbose:
                LOGGER.info('%s ↔ %s', base_chart, chart)

    return CheckResult(frozenset(orphans), frozenset(ambiguous))
