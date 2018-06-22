"""Authenticated generation of preview tokens."""

from his import authenticated, authorized

from dscms4.messages.preview import InvalidTokenType
from dscms4.orm.preview import TYPES

__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def generate(type_, ident):
    """Generates a preview token of the
    specified type for the provided ID.
    """

    try:
        token_class = TYPES[type_]
    except KeyError:
        raise InvalidTokenType()

    token = token_class.generate(ident)
    return token.token.hex


ROUTES = (
    ('GET', '/previewgen/<type_>/<int:ident>', generate,
     'generate_preview_token'),)
