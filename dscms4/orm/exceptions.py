"""Common ORM model exceptions."""

__all__ = [
    'InvalidData',
    'MissingData',
    'UnsupportedMember',
    'CircularPedigreeError',
    'OrphanedBaseChart']


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
        super().__init__()
        self.base_chart = base_chart
