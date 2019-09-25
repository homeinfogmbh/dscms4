"""Preview for deployments."""

from cmslib.presentation.deployment import Presentation
from cmslib.preview import make_response
from previewlib import preview, DeploymentPreviewToken


__all__ = ['ROUTES']


@preview(DeploymentPreviewToken)
def get_presentation(deployment):
    """Returns the presentation for the respective deployment."""

    return make_response(Presentation(deployment))


ROUTES = (('GET', '/preview/deployment', get_presentation),)
