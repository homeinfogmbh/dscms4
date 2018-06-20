"""Preview security."""


def preview():
    """Decorator to secure a WSGI function with a preview token."""

    @wraps(function)
    def wrapper(token, *args, **kwargs):
        """Receives a token and arguments for the original function."""
        try:
            PreviewToken.get
