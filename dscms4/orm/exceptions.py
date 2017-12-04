"""Common ORM model exceptions."""

__all__ = [
    'InvalidData',
    'MissingData',
    'UnsupportedMember',
    'CircularPedigreeError',
    'OrphanedBaseChart',
    'AmbiguousBaseChart',
    'QuotaExceeded',
    'NoSuchTerminal',
    'NoSuchComCatAccount',
    'NoSuchApartment']


class DSCMS4Error(Exception):
    """Base class for exceptions within the DSCMS4."""

    pass


class InvalidData(DSCMS4Error):
    """Indicates invalid ORM model data."""

    def __init__(self, invalid):
        """Sets the invalid data."""
        super().__init__(invalid)
        self.invalid = invalid


class MissingData(DSCMS4Error):
    """Indicates missing ORM model data."""

    def __init__(self, missing):
        """Sets the missing data fields."""
        super().__init__(missing)
        self.missing = missing


class UnsupportedMember(DSCMS4Error):
    """Indicates that the respective member type is unsupported."""

    def __init__(self, member):
        """Sets the respective member."""
        super().__init__(member)
        self.member = member


class CircularPedigreeError(DSCMS4Error):
    """Indicates that the a group was tried
    to be set as a child of its parents.
    """

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
