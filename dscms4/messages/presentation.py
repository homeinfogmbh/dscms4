"""Presentation related messages."""

from dscms4.messages.common import DSCMS4Message


__all__ = ['AmbiguousConfigurations', 'NoConfigurationAssigned']


class AmbiguousConfigurations(DSCMS4Message):
    """Indicates that multiple configurations
    are configured on the same level.
    """

    STATUS = 400


class NoConfigurationAssigned(DSCMS4Message):
    """Indicates that no configuration has been assigned."""

    STATUS = 400
