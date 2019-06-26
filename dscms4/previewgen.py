"""Authenticated generation of tokens for previews."""

from flask import request

from cmslib.messages.preview import INVALID_TOKEN_TYPE
from cmslib.orm.preview import TYPES
from his import authenticated, authorized
from wsgilib import JSON


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
        raise INVALID_TOKEN_TYPE

    force = 'force' in request.args
    token = token_class.generate(ident, force=force)
    token.save()
    return JSON({'token': token.token.hex})


ROUTES = (('GET', '/previewgen/<type_>/<int:ident>', generate),)
