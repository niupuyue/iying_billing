import secrets
from django.contrib.auth.hashers import MD5PasswordHasher

UNUSABLE_PASSWORD_PREFIX = '!'
UNUSABLE_PASSWORD_SUFFIX_LENGTH = 40
NOT_PROVIDED = object()
RANDOM_STRING_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
hasher = MD5PasswordHasher()


def is_password_usable(encoded):
    return encoded is None or not encoded.startswith(UNUSABLE_PASSWORD_PREFIX)


def get_random_string(length, allowed_chars=RANDOM_STRING_CHARS):
    return ''.join(secrets.choice(allowed_chars) for _ in range(length))


def iying_make_password(password):
    if not password:
        raise ValueError('密码不能为空哦~')
    salt = hasher.salt()
    return hasher.encode(password, salt)


def iying_check_password(password, encoded):
    try:
        if not is_password_usable(encoded):
            return False
        is_correct = hasher.verify(password, encoded)
        return is_correct
    except Exception as _:
        return False
