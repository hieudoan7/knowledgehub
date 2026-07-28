class AuthenticationError(Exception):
    """Raised when authentication fails."""


class EmailAlreadyExistsError(Exception):
    """Raised when a user registers with an existing email."""


class InvalidTokenError(Exception):
    """Raised when a JWT is invalid or expired."""
    