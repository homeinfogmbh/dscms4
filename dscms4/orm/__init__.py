"""Object-relational mappings.

This package provides the CMS's database models.
"""
from sys import stderr

from dscms4.orm import charts, content, chart_types, configuration, group, \
    menu, preview, settings


__all__ = ['create_tables']


# Order matters here!
MODELS = (
    charts.MODELS + configuration.MODELS + group.MODELS + menu.MODELS
    + content.MODELS + chart_types.MODELS + preview.MODELS + settings.MODELS)


def create_tables(fail_silently=True):
    """Create the respective tables."""

    for model in MODELS:
        try:
            model.create_table(fail_silently=fail_silently)
        except Exception as error:
            print('Could not create table for model "{}":\n{}.'.format(
                model, error), file=stderr)
