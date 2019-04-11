"""Preview access to presentations that bypasses
HIS authentication with token authentication.
"""

from dscms4.preview import group, system


__all__ = ['ROUTES']


ROUTES = group.ROUTES + system.ROUTES
