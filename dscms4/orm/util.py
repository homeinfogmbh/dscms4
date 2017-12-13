"""ORM utility functions."""

from collections import namedtuple
from sys import stderr

from dscms4.orm.charts import CHARTS
from dscms4.orm.charts.common import BaseChart
from dscms4.orm.exceptions import OrphanedBaseChart, AmbiguousBaseChart


__all__ = ['charts_of', 'chart_of', 'check_base_charts']


CheckResult = namedtuple('CheckResult', ('orphans', 'ambiguous'))


def charts_of(base_chart):
    """Yields all charts that associate this base chart."""

    for _, cls in CHARTS.items():
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
            print(orphaned_base_chart, file=stderr)
        except AmbiguousBaseChart as ambiguous_base_chart:
            ambiguous.append(base_chart)
            print(ambiguous_base_chart, file=stderr)
        else:
            if verbose:
                print(base_chart, '↔', chart)

    return CheckResult(orphans, ambiguous)


def delete_outdated_charts(customer):
    """Deletes outdated charts of the respective customer."""

    for chart in BaseChart.select().where(BaseChart.customer == customer):
        if not chart.active:
            # TODO: Delete chart or mark as trashed?
            #chart.delete_instance()
            #chart.trashed = True
            #chart.save()
            pass
