import random
import string
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

PIN = 0  # numbers only
NORMAL = 1  # numbers + lower case letters +
COMPLEX = 2  # numbers + lower case letters + + special characters


def encrypt(key, token):
    f = Fernet(key)
    bytes_token = token.encode('utf-8')
    return f.encrypt(bytes_token)


def decrypt(key, token):
    f = Fernet(key)
    return f.decrypt(token).decode('utf-8')

def get_key(key):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"thisMustBeConstant",
        iterations=100000,
        backend=default_backend()
    )

    return base64.urlsafe_b64encode(kdf.derive(key.encode('utf-8')))

def get_random_token(length=8, security=PIN):
    chars = None
    if security == PIN:
        chars = string.digits
    elif security == NORMAL:
        chars = string.digits + string.ascii_letters
    elif security == COMPLEX:
        chars = string.digits + string.ascii_letters + string.punctuation

    return ''.join((random.choice(chars)) for x in range(length))


def test_crypto():
    # key = Fernet.generate_key()
    password = b"this is my input password"
    # salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"thisMustBeConstant",
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))

    print("Key is: ")
    print(key)

    # print("\nencrypt hello my baby:")
    # aa = encrypt(key, "hello my baby")
    # print(aa)
    aa = b"gAAAAABYG0-fVFofY1UaWMQxH9dy8N-ZUo2NTK0firys7-TQ5rEJZ-ogenRBFcG9DC4TQFCI-uBaFaGJIllXC_ACyygQ6Tu9ug=="

    bb = decrypt(key, aa)
    print("\ndecrypt: ")
    print(bb)


if __name__ == "__main__":

    encoded_key = get_key("123")
    a = encrypt(encoded_key, "test string")
    print("Encrypted Password in db:")
    print(a)

    b = decrypt(encoded_key, a)
    print("\nDecrypted Password in db:")
    print(b)
    # test_crypto()



