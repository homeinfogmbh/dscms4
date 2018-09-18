"""Common ORM model exceptions."""


__all__ = [
    'OrphanedBaseChart',
    'AmbiguousBaseChart',
    'AmbiguousConfigurationsError',
    'NoConfigurationFound']


class DSCMS4Error(Exception):
    """Base class for exceptions within the DSCMS4."""

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


class AmbiguityError(DSCMS4Error):
    """Indicates an error due to ambiguous information."""

    pass


class AmbiguousBaseChart(AmbiguityError):
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


class AmbiguousConfigurationsError(AmbiguityError):
    """Indicates that ambiguous configurations are defined for a terminal."""

    def __init__(self, level, index):
        """Sets the level and its index."""
        super().__init__(level, index)
        self.level = level
        self.index = index


class NoConfigurationFound(DSCMS4Error):
    """Indicates that no configuration has been found."""

    pass
