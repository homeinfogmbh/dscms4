"""Preview access to presentations that bypasses
HIS authentication with token authentication.
"""

from dscms4.preview import group, terminal


__all__ = ['ROUTES']


ROUTES = group.ROUTES + terminal.ROUTES
