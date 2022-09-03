import base64
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from itertools import cycle


def encrypt_xor(file_data: bytes, key: str) -> bytes:
    return bytes(a ^ ord(b) for a, b in zip(file_data, cycle(key)))


def decrypt_xor(encrypted_data: bytes, key: str) -> bytes:
    return bytes(a ^ ord(b) for a, b in zip(encrypted_data, cycle(key)))


def encrypt(file_data: bytes, key: str):
    key = generate_key(key)
    f = Fernet(key)
    return f.encrypt(file_data)


def decrypt(encrypted_data: bytes, key: str) -> bytes:
    key = generate_key(key)
    f = Fernet(key)

    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print("Invalid token, most likely the password is incorrect")
        return

    return decrypted_data


def generate_key(password: str):
    """
    Generates a key from a `password`.
    """
    salt = generate_salt()
    derived_key = derive_key(salt, password)
    return base64.urlsafe_b64encode(derived_key)


def derive_key(salt: str, password: str):
    kdf = Scrypt(salt=salt, length=32, n=2**4, r=16, p=1)
    return kdf.derive(password.encode())


def generate_salt(size: int = 16):
    # return secrets.token_bytes(size)
    return b'\xdf\x06\xb24\x03G/Q\xfd\xa1\xf6\xf0\xc4\xf8f\xbb'
