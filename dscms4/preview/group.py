"""Preview for groups."""

from cmslib.exceptions import AmbiguousConfigurationsError
from cmslib.exceptions import NoConfigurationFound
from cmslib.messages.presentation import NO_CONFIGURATION_ASSIGNED
from cmslib.messages.presentation import AMBIGUOUS_CONFIGURATIONS
from cmslib.presentation.group import Presentation
from his.messages.request import INVALID_CONTENT_TYPE
from previewlib import preview, file_preview, GroupPreviewToken
from wsgilib import ACCEPT, JSON, XML, Binary


__all__ = ['ROUTES']


@preview(GroupPreviewToken)
def get_presentation(group):
    """Returns the presentation for the respective group."""

    presentation = Presentation(group)

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
    """Returns a file of the respective presentaion."""

    return Binary(file.bytes)


ROUTES = (
    ('GET', '/preview/group', get_presentation),
    ('GET', '/preview/group/file/<int:ident>', get_file)
)
