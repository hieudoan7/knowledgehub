from pwdlib import PasswordHash

# Configure the application's password hasher.
# By default, PasswordHash.recommended() uses Argon2id.
password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plain-text password."""

    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its hash."""

    return password_hasher.verify(password, hashed_password)

