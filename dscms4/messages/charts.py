"""Charts related messages."""

from his.messages import Message

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


class ChartsMessage(Message):
    """Base for charts related messages."""

    LOCALES = '/etc/dscms4.d/locales/charts.ini'


class ChartDataIncomplete(ChartsMessage):
    """Indicates that necessary data is missing."""

    STATUS = 400


class ChartDataInvalid(ChartsMessage):
    """Indicates that some data is invalid."""

    STATUS = 400


class NoChartTypeSpecified(ChartsMessage):
    """Indicates that no chart type has been specified."""

    STATUS = 422


class InvalidChartType(ChartsMessage):
    """Indicates that an invalid chart type has been specified."""

    STATUS = 406


class NoChartIdSpecified(ChartsMessage):
    """Indicates that no chart ID has been specified."""

    STATUS = 422


class NoSuchChart(ChartsMessage):
    """Indicates that the specified chart does not exist."""

    STATUS = 404


class NoSuchBaseChart(ChartsMessage):
    """Indicates that the respective base chart does not exist."""

    STATUS = 404


class ChartAdded(ChartsMessage):
    """Indicates that a new chart was successfully added."""

    STATUS = 201


class ChartDeleted(ChartsMessage):
    """Indicates that a chart was successfully deleted."""

    STATUS = 200


class ChartPatched(ChartsMessage):
    """Indicates that a chart was successfully patched."""

    STATUS = 200
