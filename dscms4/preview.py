"""Preview security."""

from functools import wraps

from flask import request

from hisfs import File

from dscms4.messages.preview import Unauthorized

__all__ = ['preview', 'file_preview']


def preview(token_class):
    """Decorator to secure a WSGI function with a preview token."""

    def decorator(function):
        """Decorator so secure the respective function."""

        @wraps(function)
        def wrapper(*args, **kwargs):
            """Receives a token and arguments for the original function."""
            try:
                token = token_class.get(
                    token_class.token == request.args.get('token'))
            except token_class.DoesNotExist:
                raise Unauthorized()

            return function(token.obj, *args, **kwargs)

        return wrapper

    return decorator


def file_preview(presentation_class):
    """Decorator to secure a WSGI function with a preview token."""

    def decorator(function):
        """Decorator so secure the respective function."""

        @wraps(function)
        def wrapper(obj, ident, *args, **kwargs):
            """Receives a token and arguments for the original function."""
            presentation = presentation_class(obj)

            if ident in presentation.files:
                file = File.get(
                    (File.id == ident) & (File.customer == presentation.cid))
                return function(file, *args, **kwargs)

            raise Unauthorized(files=list(presentation.files))

        return wrapper

    return decorator
