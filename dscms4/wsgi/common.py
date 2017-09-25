"""Common WSGI service base"""

from json import loads

from his.api.handlers import AuthorizedService

from ..messages import NoDataProvided, InvalidText, InvalidJSON

__all__ = ['AuthorizedJSONService']


class AuthorizedJSONService(AuthorizedService):
    """Authorizes service handling JSON data"""

    ERRORS = {
        'NO_DATA_PROVIDED': NoDataProvided(),
        'NON_UTF8_DATA': InvalidText(),
        'NON_JSON_DATA': InvalidJSON()}
