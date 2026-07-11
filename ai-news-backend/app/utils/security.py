import bcrypt

MAX_BCRYPT_PASSWORD_BYTES = 72


def _truncate_password(password: str) -> bytes:
    """Truncate password to fit within bcrypt's 72-byte limit."""
    encoded = password.encode("utf-8")
    if len(encoded) <= MAX_BCRYPT_PASSWORD_BYTES:
        return encoded
    return encoded[:MAX_BCRYPT_PASSWORD_BYTES]


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return bcrypt.hashpw(_truncate_password(password), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its bcrypt hash."""
    return bcrypt.checkpw(_truncate_password(plain_password), hashed_password.encode("utf-8"))
