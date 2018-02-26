"""Common ORM model exceptions."""

__all__ = [
    'UnsupportedMember',
    'CircularReferenceError',
    'MissingBaseChartData',
    'OrphanedBaseChart',
    'AmbiguousBaseChart',
    'QuotaExceeded',
    'NoSuchTerminal',
    'NoSuchComCatAccount',
    'NoSuchApartment']


class DSCMS4Error(Exception):
    """Base class for exceptions within the DSCMS4."""

    pass


class UnsupportedMember(DSCMS4Error):
    """Indicates that the respective member type is unsupported."""

    def __init__(self, member):
        """Sets the respective member."""
        super().__init__(member)
        self.member = member


class CircularReferenceError(DSCMS4Error):
    """Indicates that the a group was tried to be set as
    a child of its children or parent of its parents.
    """

    pass


class MissingBaseChartData(DSCMS4Error):
    """Indicates that data for the base chart is missing."""

    pass


class OrphanedBaseChart(DSCMS4Error):
    """Indicates that the respective base chart is orphaned."""

    def __init__(self, base_chart):
        """Sets the base chart."""
        super().__init__(base_chart)
        self.base_chart = base_chart

    def __str__(self):
        """Returns an appropriate message."""
        return 'Base chart {} is orphaned.'.format(self.base_chart.id)


class AmbiguousBaseChart(DSCMS4Error):
    """Indicates that the respective base chart
    is referenced by more than one chart.
    """

    def __init__(self, base_chart, references):
        """Sets the respective base chart and referencing charts."""
        super().__init__(base_chart, references)
        self.base_chart = base_chart
        self.references = references

    def __str__(self):
        """Returns an appropriate message."""
        return 'Base chart #{} is ambiguous: {}.'.format(
            self.base_chart.id, ', '.join(
                str(chart) for chart in self.references))


class QuotaExceeded(DSCMS4Error):
    """Indicates the the user quota was exceeded."""

    def __init__(self, quota):
        """Sets the quota."""
        super().__init__(quota)
        self.quota = quota


class NoSuchTerminal(DSCMS4Error):
    """Indicates that the requested terminal does not exist."""

    pass


class NoSuchComCatAccount(DSCMS4Error):
    """Indicates that the respective ComCat account does not exist."""

    pass


class NoSuchApartment(DSCMS4Error):
    """Indicates that the respective apartment does not exist."""

    pass
