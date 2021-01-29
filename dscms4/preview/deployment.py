"""Preview for deployments."""

from cmslib import DeploymentPresentation
from hwdb import Deployment
from previewlib import DeploymentPreviewToken
from previewlib import Response
from previewlib import make_response
from previewlib import preview


__all__ = ['ROUTES']


@preview(DeploymentPreviewToken)
def get_presentation(deployment: Deployment) -> Response:
    """Returns the presentation for the respective deployment."""

    return make_response(DeploymentPresentation(deployment))


ROUTES = [('GET', '/preview/deployment', get_presentation)]
