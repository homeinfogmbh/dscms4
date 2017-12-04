"""Mockups for foreign service interface implementation."""

from dscms4.orm.common import DSCMS4Model, CustomerModel

__all__ = ['ComCatAccount']


class ComCatAccount(DSCMS4Model, CustomerModel):
    """Mockup for comcat accounts."""

    pass
