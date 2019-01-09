"""Preview access to presentations that bypasses
HIS authentication with token authentication.
"""

from dscms4.preview import comcat_account, group, terminal


__all__ = ['ROUTES']


ROUTES = comcat_account.ROUTES + group.ROUTES + terminal.ROUTES
