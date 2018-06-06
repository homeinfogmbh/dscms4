"""DOM utilities."""

from uuid import uuid4

from filedb import mimetype, sha256sum

from dscms4.dom import Attachment

__all__ = ['attachment']


def attachment_dom(file_id):
    """Returns an attachment for the respective file ID."""

    if file_id is None:
        return None

    xml = Attachment()
    xml.mimetype = mimetype(file_id)
    xml.filename = str(uuid4())
    xml.sha256sum = sha256sum(file_id)
    return xml
