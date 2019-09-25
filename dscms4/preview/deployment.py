"""Preview for deployments."""

from cmslib.exceptions import AmbiguousConfigurationsError
from cmslib.exceptions import NoConfigurationFound
from cmslib.messages.presentation import NO_CONFIGURATION_ASSIGNED
from cmslib.messages.presentation import AMBIGUOUS_CONFIGURATIONS
from cmslib.presentation.deployment import Presentation
from his.messages.request import INVALID_CONTENT_TYPE
from previewlib import preview, file_preview, DeploymentPreviewToken
from wsgilib import ACCEPT, JSON, XML, Binary


__all__ = ['ROUTES']


@preview(DeploymentPreviewToken)
def get_presentation(deployment):
    """Returns the presentation for the respective deployment."""

    presentation = Presentation(deployment)

    if  'application/xml' in ACCEPT or '*/*' in ACCEPT:
        try:
            return XML(presentation.to_dom())
        except AmbiguousConfigurationsError:
            return AMBIGUOUS_CONFIGURATIONS
        except NoConfigurationFound:
            return NO_CONFIGURATION_ASSIGNED

    if 'application/json' in ACCEPT:
        return JSON(presentation.to_json())

    return INVALID_CONTENT_TYPE


@preview(DeploymentPreviewToken)
@file_preview(Presentation)
def get_file(file):
    """Returns the presentation for the respective deployment."""

    return Binary(file.bytes)


ROUTES = (
    ('GET', '/preview/deployment', get_presentation),
    ('GET', '/preview/deployment/<int:ident>', get_file)
)
