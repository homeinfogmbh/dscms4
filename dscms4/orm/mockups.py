"""Mockups for foreign service interface implementation."""

from peewee import Model

from dscms4.orm.common import CustomerModel

__all__ = ['ComCatAccount']


class ComCatAccount(Model, CustomerModel):
    """Mockup for comcat accounts."""

    pass
