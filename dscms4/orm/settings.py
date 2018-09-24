"""Per-customer Settings regarding this CMS itself.
Not to be confused with "configuration"."""
from peewee import BooleanField
from dscms4.orm.common import CustomerModel


__all__ = ['Settings']


class Settings(CustomerModel):
    """Per-customer CMS settings.
    All fields should have default values.
    """

    show_testing_terminals = BooleanField(default=False)

    @classmethod
    def for_customer(cls, customer):
        """Returns an XML DOM of the model."""
        try:
            return cls.get(cls.customer == customer)
        except cls.DoesNotExist:
            return cls(customer=customer)


MODELS = (Settings,)
