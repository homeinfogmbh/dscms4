"""Group presentations."""

from typing import Union

from cmslib.functions.group import get_group
from cmslib.presentation.group import Presentation
from his import authenticated, authorized
from wsgilib import JSON, XML, get_bool


__all__ = ['ROUTES']


@authenticated
@authorized('dscms4')
def get_presentation(ident: int) -> Union[JSON, XML]:
    """Returns the presentation for the respective deployment."""

    presentation = Presentation(get_group(ident))

    if get_bool('xml'):
        return XML(presentation.to_dom())

    return JSON(presentation.to_json())


ROUTES = [('GET', '/group/<int:ident>/presentation', get_presentation)]
