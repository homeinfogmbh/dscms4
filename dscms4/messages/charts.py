"""Charts related messages."""

from dscms4.messages.common import DSCMS4Message

__all__ = [
    'ChartDataIncomplete',
    'ChartDataInvalid',
    'NoChartTypeSpecified',
    'InvalidChartType',
    'NoChartIdSpecified',
    'NoSuchChart',
    'NoSuchBaseChart',
    'ChartAdded',
    'ChartDeleted',
    'ChartPatched']


class ChartDataIncomplete(DSCMS4Message):
    """Indicates that necessary data is missing."""

    STATUS = 400


class ChartDataInvalid(DSCMS4Message):
    """Indicates that some data is invalid."""

    STATUS = 400


class NoChartTypeSpecified(DSCMS4Message):
    """Indicates that no chart type has been specified."""

    STATUS = 422


class InvalidChartType(DSCMS4Message):
    """Indicates that an invalid chart type has been specified."""

    STATUS = 406


class NoChartIdSpecified(DSCMS4Message):
    """Indicates that no chart ID has been specified."""

    STATUS = 422


class NoSuchChart(DSCMS4Message):
    """Indicates that the specified chart does not exist."""

    STATUS = 404


class NoSuchBaseChart(DSCMS4Message):
    """Indicates that the respective base chart does not exist."""

    STATUS = 404


class ChartAdded(DSCMS4Message):
    """Indicates that a new chart was successfully added."""

    STATUS = 201


class ChartDeleted(DSCMS4Message):
    """Indicates that a chart was successfully deleted."""

    STATUS = 200


class ChartPatched(DSCMS4Message):
    """Indicates that a chart was successfully patched."""

    STATUS = 200
