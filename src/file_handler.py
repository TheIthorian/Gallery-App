import base64
import io
import os
from PIL import Image as PILImage
import requests

from user import UserProfile
from encryption import decrypt, decrypt_xor, encrypt, encrypt_xor

MAX_WIDTH = 800


def save_image_to_file(url: str, filename: str, userProfile: UserProfile, encryption_mode='Fernet') -> PILImage:
    image_data = rescale_image(PILImage.open(
        requests.get(url, stream=True).raw))

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, '..', 'images', filename + '.img')

    if encryption_mode == 'xor':
        encrypted_data = encrypt_xor(
            image_data.tobytes(), userProfile.password)
    else:
        encrypted_data = encrypt(image_data.tobytes(), userProfile.password)

    with open(file_path, "xb") as file:
        file.write(encrypted_data)

    return image_data


def rescale_image(image: PILImage) -> PILImage:
    if image.size[0] > MAX_WIDTH:
        width_percent = MAX_WIDTH / float(image.size[0])
        height = int((float(image.size[1]) * float(width_percent)))
        return image.resize((MAX_WIDTH, height), PILImage.ANTIALIAS)

    return image


def get_image_from_file(filename: str, userProfile: UserProfile, mode, width, height, encryption_mode='Fernet') -> base64:
    if (filename is None or filename == 'xx'):
        return None

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, '..', 'images', filename + '.img')

    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    if encryption_mode == 'xor':
        image_data = decrypt_xor(encrypted_data, userProfile.password)
    else:
        image_data = decrypt(encrypted_data, userProfile.password)

    if image_data is None:
        return None

    image = PILImage.frombytes(
        mode=mode, size=[width, height], data=image_data)

    image_file = io.BytesIO()
    image.save(image_file, format="PNG")
    img = base64.b64encode(image_file.getvalue()).decode('ascii')

    return img


def replace_image(url: str, filename: str, userProfile: UserProfile) -> PILImage:
    image_data = rescale_image(PILImage.open(
        requests.get(url, stream=True).raw))

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, '..', 'images', filename + '.img')

    remove_image(filename)

    encrypted_data = encrypt(image_data.tobytes(), userProfile.password)

    with open(file_path, "xb") as file:
        file.write(encrypted_data)

    return image_data


def remove_image(filename: str):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, '..', 'images', filename + '.img')

    if os.path.exists(file_path):
        os.remove(file_path)
