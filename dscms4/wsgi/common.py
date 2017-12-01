"""Common WSGI service base."""

from his.api.handlers import service, AuthorizedService

from dscms4.wsgi.messages import NoDataProvided, InvalidText, InvalidJSON

__all__ = ['DSCMS4Service']


@service('dscms4')
class DSCMS4Service(AuthorizedService):
    """Authorizes service handling JSON data."""

    ERRORS = {
        'NO_DATA_PROVIDED': NoDataProvided(),
        'NON_UTF8_DATA': InvalidText(),
        'NON_JSON_DATA': InvalidJSON()}
