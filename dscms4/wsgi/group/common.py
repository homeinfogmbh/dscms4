"""Common functions."""

from his import CUSTOMER

from dscms4.messages.group import NoSuchGroup
from dscms4.orm.group import Group


__all__ = ['get_group']


def get_group(ident):
    """Returns the respective group of the current customer."""

    try:
        return Group.get((Group.customer == CUSTOMER.id) & (Group.id == ident))
    except Group.DoesNotExist:
        raise NoSuchGroup()
