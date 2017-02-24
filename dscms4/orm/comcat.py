"""ComCat stuff"""

# XXX: Outsource this to own HIS module
from peewee import DoesNotExist, CharField, ForeignKeyField, BooleanField
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from homeinfo.lib.log import Logger
from his.orm import module_model
from his.mods.dscms4.orm.company import RentalUnit


class AccountExists(Exception):
    """Indicates that an account with the
    respective user name already exists
    """

    pass


class NoSuchAccount(Exception):
    """Indicates that the respective account does not exist"""

    pass


class InvalidCredentials(Exception):
    """Indicates that user name and / or password were wrong"""

    pass


class NoAccountAssociated(Exception):
    """Indicates that no actual account is
    associated with the specified account data
    """

    pass


class ComCatModel(module_model('comcat')):
    """Basic model for ComCat"""

    def __init__(self, *args, logger=None, **kwargs):
        """Adds a logger to the instance"""
        super().__init__(*args, **kwargs)

        if logger is None:
            self.logger = Logger(self.__class__.__name__)
        else:
            self.logger = logger.inherit(self.__class__.__name__)


class BaseAccount(ComCatModel):
    """Base account data"""

    class Meta:
        db_table = 'account'

    PASSWORD_HASHER = PasswordHasher()

    user = CharField(255)
    passwd = CharField(255)
    locked = BooleanField(default=False)

    @classmethod
    def add(cls, user, passwd, locked=False):
        """Creates a new account"""
        try:
            cls.get(cls.user == user)
        except DoesNotExist:
            account = cls()
            account.user == user
            account.passwd = cls.PASSWORD_HASHER.hash(passwd)
            account.locked = locked
            account.save()
            return account
        else:
            raise AccountExists()

    @classmethod
    def login(cls, user, passwd):
        """Logs in an account"""
        try:
            account = cls.get(cls.user == user)
        except DoesNotExist:
            raise NoSuchAccount()
        else:
            if account.authenticate(passwd):
                return account
            else:
                raise InvalidCredentials()

    def authenticate(self, passwd):
        """Checks the given password"""
        try:
            return self.PASSWORD_HASHER.verify(self.passwd, passwd)
        except VerifyMismatchError:
            return False


class _Account(ComCatModel):
    """Abstract account base for tenants and providers"""

    account = ForeignKeyField(BaseAccount, db_column='account')

    @classmethod
    def login(cls, user, passwd):
        """Logs in an account"""
        account = BaseAccount.login(user, passwd)

        try:
            return cls.get(cls.account == account)
        except DoesNotExist:
            raise NoAccountAssociated()


class Tenant(_Account):
    """Tenant accounts"""

    rental_unit = ForeignKeyField(RentalUnit, db_column='rental_unit')

    @classmethod
    def add(cls, rental_unit, user, passwd, locked=False):
        """Adds tenant account"""
        account = BaseAccount.add(user, passwd, locked=locked)
        tenant = cls()
        tenant.account = account
        tenant.rental_unit = rental_unit
        tenant.save()
        return tenant

    def move(self, rental_unit):
        """Moves the account to another rental unit"""
        self.rental_unit = rental_unit
        self.save()
        return self


class ServiceProvider(_Account):
    """Service provider accounts"""

    class Meta:
        db_table = 'service_provider'

    customer = ForeignKeyField(RentalUnit, db_column='customer')

    @classmethod
    def add(cls, customer, user, passwd, locked=False):
        """Adds tenant account"""
        account = BaseAccount.add(user, passwd, locked=locked)
        service_provider = cls()
        service_provider.account = account
        service_provider.customer = customer
        service_provider.save()
        return service_provider
