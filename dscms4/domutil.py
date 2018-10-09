"""DOM utilities."""

from hisfs import File

from dscms4.dom import Attachment


__all__ = ['attachment_dom']


def attachment_dom(ident, format=None, index=None):
    """Returns an attachment for the respective file ID."""

    if ident is None:
        return None

    try:
        file = File[ident]
    except File.DoesNotExist:
        return None

    xml = Attachment()
    xml.id = file.id
    xml.mimetype = file.mimetype
    xml.filename = file.name
    xml.sha256sum = file.sha256sum
    xml.format = format
    xml.index = index
    return xml
