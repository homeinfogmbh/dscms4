"""Object relatinal mappings.

This package provides the CMS's database models.
"""
from sys import stderr

from dscms4.orm import charts, content, configuration, group, menu

__all__ = ['create_tables']


# Order matters here!
MODELS = (
    charts.MODELS + configuration.MODELS + group.MODELS + menu.MODELS
    + content.MODELS)


def create_tables(fail_silently=True):
    """Create the respective tables."""

    for model in MODELS:
        try:
            model.create_table(fail_silently=fail_silently)
        except Exception as error:
            print('Could not create table for model "{}":\n{}.'.format(
                model, error), file=stderr)
