"""Preview for a terminal."""

from dscms4.orm.preview import TerminalPreviewToken

__all__ = ['ROUTES']


@with_terminal
@preview(TerminalPreviewToken)
def get_presentation(terminal):
    """Returns the presentation for the respective terminal."""

    try:
        request.args['xml']
    except KeyError:
        return JSON(presentation(terminal))

    try:
        presentation_dom = presentation(terminal, xml=True)
    except NoConfigurationFound:
        return NoConfigurationAssigned()

    return XML(presentation_dom)


@with_terminal
@preview(TerminalPreviewToken)
@attachments
def get_presentation(terminal):
    """Returns the presentation for the respective terminal."""

    try:
        request.args['xml']
    except KeyError:
        return JSON(presentation(terminal))

    try:
        presentation_dom = presentation(terminal, xml=True)
    except NoConfigurationFound:
        return NoConfigurationAssigned()

    return XML(presentation_dom)
