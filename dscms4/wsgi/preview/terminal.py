"""Preview for a terminal."""

from flask import request

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

    try:
        request.args['xml']
    except KeyError:
        return JSON(presentation.to_dict())

    try:
        return XML(presentation.to_dom())
    except NoConfigurationFound:
        return NoConfigurationAssigned()


@preview(TerminalPreviewToken)
@file_preview(Presentation)
def get_file(file):
    """Returns the presentation for the respective terminal."""

    return Binary(file.bytes)


ROUTES = (
    ('GET', '/preview/terminal/<int:tid>', get_presentation,
     'preview_terminal_presentation'),
    ('GET', '/preview/terminal/<int:tid>/file/<int:ident>', get_file,
     'preview_terminal_file'))
