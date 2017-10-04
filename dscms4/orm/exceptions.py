"""Common ORM model exceptions."""

__all__ = ['InvalidData', 'MissingData', 'UnsupportedMember']


class InvalidData(Exception):
    """Indicates invalid ORM model data."""

    def __init__(self, invalid):
        """Sets the invalid data."""
        super().__init__(invalid)
        self.invalid = invalid


class MissingData(Exception):
    """Indicates missing ORM model data."""

    def __init__(self, missing):
        """Sets the missing data fields."""
        super().__init__(missing)
        self.missing = missing


class UnsupportedMember(Exception):
    """Indicates that the respective member type is unsupported."""

    def __init__(self, member):
        """Sets the respective member."""
        super().__init__(member)
        self.member = member
