"""Common ORM models"""

from homeinfo.lib.log import Logger
from his.orm import module_model


class DSCMS4Model(module_model('dscms4')):
    """Basic ORM model for ComCat"""

    def __init__(self, *args, logger=None, **kwargs):
        """Adds a logger to the instance"""
        super().__init__(*args, **kwargs)

        if logger is None:
            self.logger = Logger(self.__class__.__name__)
        else:
            self.logger = logger.inherit(self.__class__.__name__)
