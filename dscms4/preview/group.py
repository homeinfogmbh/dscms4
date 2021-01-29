"""Preview for groups."""

from cmslib.orm.group import Group
from cmslib.presentation.group import Presentation
from previewlib import GroupPreviewToken
from previewlib import Response
from previewlib import make_response
from previewlib import preview


__all__ = ['ROUTES']


@preview(GroupPreviewToken)
def get_presentation(group: Group) -> Response:
    """Returns the presentation for the respective group."""

    return make_response(Presentation(group))


ROUTES = [('GET', '/preview/group', get_presentation)]
