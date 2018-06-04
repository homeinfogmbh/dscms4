"""Common WSGI functions."""

from flask import request

__all__ = ['get_brief']


def get_brief():
    """Returns whether a brief data set is requested."""

    try:
        request.args['brief']
    except KeyError:
        return False

    return True
