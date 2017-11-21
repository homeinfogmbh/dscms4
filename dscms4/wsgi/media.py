"""User's media files."""


@service('dscms4')
@routed('/media/[id:int]')
class MediaHandler(DSCMS4Service):
    """Handles user's media files."""

    @property
    def files(self):
        """Yields all files of the respective customer."""
        return MediaFile.select().where(MediaFile.customer == self.customer)

    @property
    def file(self):
        """Returns the selected file."""
        return MediaFile.get(
            (MediaFile.id == self.vars['id'])
            & (MediaFile.customer == self.customer))

    def list(self):
        """Lists available media files."""
        return JSON([file.to_dict() for file in self.files])

    def get(self):
        """Returns media files."""
        if self.vars['id'] is None:
            return self.list()

        return JSON(self.file.to_dict())
