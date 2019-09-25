"""Preview for deployments."""

from cmslib.exceptions import AmbiguousConfigurationsError
from cmslib.exceptions import NoConfigurationFound
from cmslib.messages.presentation import NO_CONFIGURATION_ASSIGNED
from cmslib.messages.presentation import AMBIGUOUS_CONFIGURATIONS
from cmslib.presentation.deployment import Presentation
from his.messages.request import INVALID_CONTENT_TYPE
from previewlib import preview, file_preview, DeploymentPreviewToken
from tenant2tenant import TenantMessage
from tenant2tenant.dom import tenant2tenant     # pylint: disable=E0401,E0611
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


@preview(DeploymentPreviewToken)
def get_tenant2tenant(deployment):
    """Returns the tenant-to-tenant
    messages for the requested deployment.
    """

    messages = TenantMessage.for_deployment(deployment)

    if  'application/xml' in ACCEPT or '*/*' in ACCEPT:
        xml = tenant2tenant()

        for message in messages:
            xml.message.append(message.to_dom())

        return XML(xml)

    if 'application/json' in ACCEPT:
        return JSON([message.to_json() for message in messages])

    return INVALID_CONTENT_TYPE


ROUTES = (
    ('GET', '/preview/deployment', get_presentation),
    ('GET', '/preview/deployment/file/<int:ident>', get_file),
    ('GET', '/preview/deployment/tenant2tenant', get_tenant2tenant)
)
