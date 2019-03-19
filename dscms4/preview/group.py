"""Preview for groups."""

from cmslib.exceptions import AmbiguousConfigurationsError
from cmslib.exceptions import NoConfigurationFound
from cmslib.messages.presentation import NO_CONFIGURATION_ASSIGNED
from cmslib.messages.presentation import AMBIGUOUS_CONFIGURATIONS
from cmslib.orm.preview import GroupPreviewToken
from cmslib.presentation.group import Presentation
from cmslib.preview import preview, file_preview
from his.messages.request import INVALID_CONTENT_TYPE
from tenant2tenant import TenantMessage
from tenant2tenant.dom import tenant2tenant     # pylint: disable=E0401,E0611
from wsgilib import ACCEPT, JSON, XML, Binary


__all__ = ['ROUTES']


@preview(GroupPreviewToken)
def get_presentation(terminal):
    """Returns the presentation for the respective terminal."""

    presentation = Presentation(terminal)

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


@preview(GroupPreviewToken)
@file_preview(Presentation)
def get_file(file):
    """Returns the presentation for the respective terminal."""

    return Binary(file.bytes)


@preview(GroupPreviewToken)
def get_tenant2tenant(terminal):
    """Returns the tenant-to-tenant messages for the requested terminal."""

    messages = TenantMessage.for_terminal(terminal)

    if  'application/xml' in ACCEPT or '*/*' in ACCEPT:
        xml = tenant2tenant()

        for message in messages:
            xml.message.append(message.to_dom())

        return XML(xml)

    if 'application/json' in ACCEPT:
        return JSON([message.to_json() for message in messages])

    return INVALID_CONTENT_TYPE


ROUTES = (
    ('GET', '/preview/group', get_presentation,
     'preview_group_presentation'),
    ('GET', '/preview/group/file/<int:ident>', get_file, 'preview_group_file'),
    ('GET', '/preview/group/tenant2tenant', get_tenant2tenant,
     'preview_group_tenant2tenant'))
