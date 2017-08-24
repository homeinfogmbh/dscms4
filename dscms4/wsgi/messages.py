"""WSGI message definitions"""

from his.api.messages import locales, HISMessage

__all__ = [
    'MissingData',
    'NoChartTypeSpecified',
    'InvalidChartType',
    'NoChartIdSpecified',
    'NoSuchChart',
    'ChartAdded',
    'ChartDeleted']


@locales('/etc/his.d/locale/dscms4.ini')
class DSCMS4Message(HISMessage):
    """Basic real estates message"""

    pass


class MissingData(DSCMS4Message):
    """Indicates that necessary data is missing"""

    STATUS = 400


class NoChartTypeSpecified(DSCMS4Message):
    """Indicates that no chart type has been specified"""

    STATUS = 422


class InvalidChartType(DSCMS4Message):
    """Indicates that an invalid chart type has been specified"""

    STATUS = 406


class NoChartIdSpecified(DSCMS4Message):
    """Indicates that no chart ID has been specified"""

    STATUS = 422


class NoSuchChart(DSCMS4Message):
    """Indicates that the specified chart does not exist"""

    STATUS = 404


class ChartAdded(DSCMS4Message):
    """Indicates that a new chart was successfully added"""

    STATUS = 201


class ChartDeleted(DSCMS4Message):
    """Indicates that a chart was successfully deleted"""

    STATUS = 200
