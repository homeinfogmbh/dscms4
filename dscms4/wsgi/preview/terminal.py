"""Preview for a terminal."""

from flask import request

from digsigdb import TenantMessage
from digsigdb.dom import tenant2tenant
from wsgilib import JSON, XML, Binary

from dscms4.content.exceptions import NoConfigurationFound
from dscms4.content.terminal.presentation import Presentation
from dscms4.messages.content import NoConfigurationAssigned
from dscms4.orm.preview import TerminalPreviewToken
from dscms4.preview import preview, file_preview


__all__ = ['ROUTES']


@preview(TerminalPreviewToken)
def get_presentation(terminal):
    """Returns the presentation for the respective terminal."""

    presentation = Presentation(terminal)

    if 'xml' in request.args:
        try:
            return XML(presentation.to_dom())
        except NoConfigurationFound:
            return NoConfigurationAssigned()

    return JSON(presentation.to_json())



@preview(TerminalPreviewToken)
@file_preview(Presentation)
def get_file(file):
    """Returns the presentation for the respective terminal."""

    return Binary(file.bytes)



@preview(TerminalPreviewToken)
def get_tenant2tenant(terminal):
    """Returns the tenant-to-tenant messages for the requested terminal."""

    messages = TenantMessage.for_terminal(terminal)

    if 'xml' in request.args:
        xml = tenant2tenant()

        for message in messages:
            xml.message.append(message.to_dom())

        return XML(xml)

    return JSON([message.to_json() for message in messages])


ROUTES = (
    ('GET', '/preview/terminal', get_presentation,
     'preview_terminal_presentation'),
    ('GET', '/preview/file/<int:ident>', get_file, 'preview_terminal_file'),
    ('GET', '/preview/tenant2tenant', get_tenant2tenant,
     'preview_tenant2tenant'))
