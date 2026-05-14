from passlib.context import CryptContext


_password_context = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return _password_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return _password_context.verify(plain_password, password_hash)