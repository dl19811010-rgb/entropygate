from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MAX_BCRYPT_PASSWORD_BYTES = 72


def _truncate_password(password: str) -> str:
    """Truncate password to fit within bcrypt's 72-byte limit."""
    encoded = password.encode("utf-8")
    if len(encoded) <= MAX_BCRYPT_PASSWORD_BYTES:
        return password
    return encoded[:MAX_BCRYPT_PASSWORD_BYTES].decode("utf-8", errors="ignore")


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return pwd_context.hash(_truncate_password(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its bcrypt hash."""
    return pwd_context.verify(_truncate_password(plain_password), hashed_password)
