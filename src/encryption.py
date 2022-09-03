import base64
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

def encrypt_xor(filename: str, file_data: bytes, password: str):
    from itertools import cycle

    encrypted_data = bytes(a ^ ord(b) for a, b in zip(file_data, cycle(password)))
    
    with open(filename, "xb") as file:
        file.write(encrypted_data)


def decrypt_xor(filename: str, password: str):
    from itertools import cycle

    with open(filename, "rb") as file:
        encrypted_data = file.read()
    
    return bytes(a ^ ord(b) for a, b in zip(encrypted_data, cycle(password)))


def encrypt(file_data: bytes, password: str):
    """
    Encrypts the file_data and write it to file
    """
    key = generate_key(password)
    f = Fernet(key)
    return f.encrypt(file_data)    


def decrypt(encrypted_data: str, password: str) -> bytes:
    """
    Given a filename (str) and key (bytes), it decrypts the file
    """
    key = generate_key(password)
    f = Fernet(key)

    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print("Invalid token, most likely the password is incorrect")
        return

    return decrypted_data


def derive_key(salt: str, password: str):
    """Derive the key from the `password` using the passed `salt`"""
    kdf = Scrypt(salt=salt, length=32, n=2**2, r=16, p=1)
    return kdf.derive(password.encode())

def generate_salt(size=16):
    # return secrets.token_bytes(size)
    return b'\xdf\x06\xb24\x03G/Q\xfd\xa1\xf6\xf0\xc4\xf8f\xbb'

def load_salt():
    # load salt from salt.salt file
    return open("salt.salt", "rb").read()

def generate_key(password):
    """
    Generates a key from a `password`.
    """
    salt = generate_salt()
    
    # generate the key from the salt and the password
    derived_key = derive_key(salt, password)

    # encode it using Base 64 and return it
    return base64.urlsafe_b64encode(derived_key)