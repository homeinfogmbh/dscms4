"""Preview for groups."""

from his.messages import InvalidContentType
from tenant2tenant import TenantMessage
from tenant2tenant.dom import tenant2tenant
from wsgilib import ACCEPT, JSON, XML, Binary

from dscms4.exceptions import AmbiguousConfigurationsError
from dscms4.exceptions import NoConfigurationFound
from dscms4.messages.presentation import NoConfigurationAssigned
from dscms4.messages.presentation import AmbiguousConfigurations
from dscms4.orm.preview import GroupPreviewToken
from dscms4.presentation.group import Presentation
from dscms4.preview import preview, file_preview


__all__ = ['ROUTES']


@preview(GroupPreviewToken)
def get_presentation(terminal):
    """Returns the presentation for the respective terminal."""

    presentation = Presentation(terminal)

    if  'application/xml' in ACCEPT or '*/*' in ACCEPT:
        try:
            return XML(presentation.to_dom())
        except AmbiguousConfigurationsError:
            return AmbiguousConfigurations()
        except NoConfigurationFound:
            return NoConfigurationAssigned()

    if 'application/json' in ACCEPT:
        return JSON(presentation.to_json())

    return InvalidContentType()


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

    return InvalidContentType()


ROUTES = (
    ('GET', '/preview/group', get_presentation,
     'preview_group_presentation'),
    ('GET', '/preview/group/file/<int:ident>', get_file, 'preview_group_file'),
    ('GET', '/preview/group/tenant2tenant', get_tenant2tenant,
     'preview_group_tenant2tenant'))
