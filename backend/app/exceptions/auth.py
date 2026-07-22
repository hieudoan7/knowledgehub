class AuthenticationError(Exception):
    """Raised when authentication fails."""


class EmailAlreadyExistsError(Exception):
    """Raised when a user registers with an existing email."""
