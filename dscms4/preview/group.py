"""Preview for groups."""

from cmslib import Group, GroupPresentation
from previewlib import GroupPreviewToken
from previewlib import Response
from previewlib import make_response
from previewlib import preview


__all__ = ['ROUTES']


@preview(GroupPreviewToken)
def get_presentation(group: Group) -> Response:
    """Returns the presentation for the respective group."""

    return make_response(GroupPresentation(group))


ROUTES = [('GET', '/preview/group', get_presentation)]
