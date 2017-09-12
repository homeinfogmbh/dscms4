"""Configurations."""

from contextlib import suppress

from peewee import Model, ForeignKeyField, TimeField, DecimalField

from .common import DSCMS4Model, CustomerModel

__all__ = ['Configuration']


def percentage(value):
    """Returns the percentage of a decimal number."""

    if 0 <= value <= 100:
        return value

    raise ValueError('Invalid percentage: {}/{}.'.format(value, type(value)))


def stripped_time_str(time):
    """Returns the hour and minute string
    representation of the provided time.
    """

    return '{}:{}'.format(time.hour, time.minute)


class Configuration(Model, CustomerModel):
    """Customer configuration for charts"""

    # TODO: Add configurations for all possible charts

    def to_dict(self):
        """Converts the configuration into a JSON-like dictionary."""
        dictionary = {}
        backlight = {}

        for backlight in Backlight.select().where(
                Backlight.configuration == self):
            with suppress(ValueError):
                backlight.update(backlight.to_dict())

        dictionary['backlight'] = backlight
        return dictionary


class Backlight(Model, DSCMS4Model):
    """Backlight beightness settings of the respective configuration."""

    configuration = ForeignKeyField(Configuration, db_column='configuration')
    time = TimeField()
    value = DecimalField(3, 2)

    @classmethod
    def add(cls, configuration, time, value=None, percent=None):
        """Adds a new backlight setting."""
        record = cls()
        record.configuration = configuration
        record.time = time

        if value is not None and percent is not None:
            raise ValueError('Must specify either value or percent.')
        elif value is not None:
            record.value = value
        elif percent is not None:
            record.percent = percent
        else:
            raise ValueError('Must specify either value or percent.')

        record.save()
        return record

    @property
    def percent(self):
        """Returns the percentage as an integer."""
        return percentage(int(self.value * 100))

    @percent.setter
    def percent(self, value):
        """Sets the percentage."""
        self.value = percentage(value) / 100

    def to_dict(self):
        """Returns the backlight as dictionary."""
        return {stripped_time_str(self.time): self.percent}
