"""Preview for groups."""

from cmslib.orm.group import Group
from cmslib.presentation.group import Presentation
from cmslib.preview import Response, make_response
from previewlib import preview, GroupPreviewToken


__all__ = ['ROUTES']


@preview(GroupPreviewToken)
def get_presentation(group: Group) -> Response:
    """Returns the presentation for the respective group."""

    return make_response(Presentation(group))


ROUTES = (('GET', '/preview/group', get_presentation),)
