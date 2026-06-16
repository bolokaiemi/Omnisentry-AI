
import base64


def encrypt_data(data: str):

    encoded = base64.b64encode(
        data.encode()
    ).decode()

    return encoded


def decrypt_data(encoded: str):

    decoded = base64.b64decode(
        encoded.encode()
    ).decode()

    return decoded

