"""Configuration related messages."""

from dscms4.messages.common import DSCMS4Message

__all__ = [
    'NoSuchConfiguration',
    'ConfigurationAdded',
    'ConfigurationPatched',
    'ConfigurationDeleted']


class NoSuchConfiguration(DSCMS4Message):
    """Indicates that the respective configuration was not found."""

    STATUS = 404


class ConfigurationAdded(DSCMS4Message):
    """indicates that the configuration was successfully added."""

    STATUS = 201


class ConfigurationPatched(DSCMS4Message):
    """Indicates that the configuration was successfully patched."""

    STATUS = 200


class ConfigurationDeleted(DSCMS4Message):
    """Indicates that the configuration was successfully deleted."""

    STATUS = 200
