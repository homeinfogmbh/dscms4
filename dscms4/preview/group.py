"""Preview for groups."""

from cmslib.presentation.group import Presentation
from cmslib.preview import make_response
from previewlib import preview, GroupPreviewToken


__all__ = ['ROUTES']


@preview(GroupPreviewToken)
def get_presentation(group):
    """Returns the presentation for the respective group."""

    return make_response(Presentation(group))


ROUTES = (('GET', '/preview/group', get_presentation),)
