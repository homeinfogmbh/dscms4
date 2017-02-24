"""ComCat stuff"""

from peewee import CharField, ForeignKeyField, BooleanField
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from homeinfo.lib.log import Logger
from his.orm import module_model
from his.mods.dscms4.orm.company import RentalUnit


class ComCatModel(module_model('comcat')):
    """Basic model for ComCat"""

    def __init__(self, *args, logger=None, **kwargs):
        """Adds a logger to the instance"""
        super().__init__(*args, **kwargs)

        if logger is None:
            self.logger = Logger(self.__class__.__name__)
        else:
            self.logger = logger.inherit(self.__class__.__name__)


class TenantAccount(ComCatModel):
    """Accounts for tenants"""

    class Meta:
        db_table = 'tenant_account'

    PASSWORD_HASHER = PasswordHasher()

    user = CharField(255)
    passwd = CharField(255)
    rental_unit = ForeignKeyField(RentalUnit, db_column='rental_unit')
    locked = BooleanField(default=False)

    def authenticate(self, passwd):
        """Checks the given password"""
        try:
            return self.PASSWORD_HASHER.verify(self.passwd, passwd)
        except VerifyMismatchError:
            return False
