"""Configuration related messages."""

from his.messages import Message

__all__ = [
    'NoSuchConfiguration',
    'ConfigurationAdded',
    'ConfigurationPatched',
    'ConfigurationDeleted']


class ConfigurationMessage(Message):
    """Base class for configuration related messages."""

    LOCALES = '/etc/dscms4.d/locales/configuration.ini'


class NoSuchConfiguration(ConfigurationMessage):
    """Indicates that the respective configuration was not found."""

    STATUS = 404


class ConfigurationAdded(ConfigurationMessage):
    """indicates that the configuration was successfully added."""

    STATUS = 201


class ConfigurationPatched(ConfigurationMessage):
    """Indicates that the configuration was successfully patched."""

    STATUS = 200


class ConfigurationDeleted(ConfigurationMessage):
    """Indicates that the configuration was successfully deleted."""

    STATUS = 200
