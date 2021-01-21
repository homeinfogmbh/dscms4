"""Customers lising interface."""

from peewee import ModelSelect

from his import authenticated, authorized, root
from mdb import Company, Customer
from wsgilib import JSON


__all__ = ['ROUTES']


def get_customers() -> ModelSelect:
    """Selects all customers."""

    return Customer.select(Customer, Company).join(Company).where(True)


@authenticated
@authorized('dscms4')
@root
def list_() -> JSON:
    """Lists customers."""

    return JSON([record.to_json(cascade=True) for record in get_customers()])


ROUTES = [('GET', '/customers', list_)]
