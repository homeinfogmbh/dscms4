"""Legacy API for HOMEINFO smart TVs."""

from flask import Flask

from cmslib.presentation.deployment import Presentation
from cmslib.preview import Response, make_response
from hwdb import Deployment, SmartTV
from wsgilib import get_int


__all__ = ['APPLICATION', 'get_smart_tv']


APPLICATION = Flask('expose-tv')


def get_smart_tv():
    """Returns the requested smart TV."""

    condition = Deployment.customer == get_int('knr')
    condition &= SmartTV.id == get_int('monitorid')
    return SmartTV.select(cascade=True).where(condition).get()


@APPLICATION.route('/presentation', methods=['GET'], strict_slashes=False)
def get_presentation() -> Response:
    """Returns the presentation as XML."""

    smart_tv = get_smart_tv()
    return make_response(Presentation(smart_tv.deployment))


@APPLICATION.errorhandler(SmartTV.DoesNotExist)
def handle_smart_tv_not_found(_: SmartTV.DoesNotExist):
    """Handles not found smart TVs."""

    return ('Smart TV not found.', 404)
