"""Common WSGI service base"""

from json import loads

from his.api.handlers import AuthorizedService

from ..messages import NoDataProvided, InvalidText, InvalidJSON

__all__ = ['AuthorizedJSONService']


class AuthorizedJSONService(AuthorizedService):
    """Authorizes service handling JSON data"""

    @property
    def text(self):
        """Returns POST-ed text"""
        try:
            return self.data.decode()
        except TypeError:
            raise NoDataProvided() from None
        except ValueError:
            raise InvalidText() from None

    @property
    def json(self):
        """Returns POST-ed JSON data"""
        try:
            return loads(self.text)
        except ValueError:
            raise InvalidJSON() from None
