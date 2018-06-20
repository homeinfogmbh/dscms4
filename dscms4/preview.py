"""Preview security."""

from functools import wraps

from flask import request

from his import CUSTOMER

from dscms4.messages.preview import Unauthorized

__all__ = ['preview', 'file_preview']


def preview(token_class):
    """Decorator to secure a WSGI function with a preview token."""

    def decorator(function):
        """Decorator so secure the respective function."""

        @wraps(function)
        def wrapper(obj, *args, **kwargs):
            """Receives a token and arguments for the original function."""
            try:
                token_class.fetch(request.args.get('token'), CUSTOMER.id, obj)
            except token_class.DoesNotExist:
                raise Unauthorized()

            return function(obj, *args, **kwargs)

        return wrapper

    return decorator


def file_preview(presentation_class):
    """Decorator to secure a WSGI function with a preview token."""

    def decorator(function):
        """Decorator so secure the respective function."""

        @wraps(function)
        def wrapper(obj, file_id, *args, **kwargs):
            """Receives a token and arguments for the original function."""
            presentation = presentation_class(obj)

            if file_id in presentation.files:
                return function(file_id, *args, **kwargs)

            raise Unauthorized

        return wrapper

    return decorator
