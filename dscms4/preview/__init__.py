"""Preview access to presentations that bypasses
HIS authentication with token authentication.
"""

from dscms4.preview import deployment, group


__all__ = ['ROUTES']


ROUTES = deployment.ROUTES + group.ROUTES
