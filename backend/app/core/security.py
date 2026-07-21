from pwdlib import PasswordHash

# Configure the application's password hasher.
# By default, PasswordHash.recommended() uses Argon2id.
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plain-text password."""

    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its hash."""

    return password_hash.verify(password, hashed_password)

