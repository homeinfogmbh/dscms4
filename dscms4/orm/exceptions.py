"""Common ORM model exceptions"""

__all__ = ['InvalidData', 'MissingData']


class InvalidData(Exception):
    """indicates invalid ORM model data"""

    def __init__(self, invalid):
        """Sets the invalid data"""
        super().__init__(invalid)
        self.invalid = invalid


class MissingData(Exception):
    """indicates missing ORM model data"""

    def __init__(self, missing):
        """Sets the missing data"""
        super().__init__(missing)
        self.missing = missing
