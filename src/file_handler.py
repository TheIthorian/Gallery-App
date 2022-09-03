import base64
import io
import os
from PIL import Image
import requests

from user import UserProfile
from encryption import decrypt, encrypt

def save_image_to_file(url: str, filename: str, userProfile: UserProfile) -> Image:
    image_data = Image.open(requests.get(url, stream=True).raw)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, '..', 'images', filename + '.img')

    encrypted_data = encrypt(image_data.tobytes(), userProfile.password)

    with open(file_path, "xb") as file:
        file.write(encrypted_data)

    return image_data


def get_image_from_file(filename: str, userProfile: UserProfile, mode, width, height) -> base64:
    print(f"get_image_from_file: {filename}")

    if (filename is None or filename == 'xx'):
        return None

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, '..', 'images', filename + '.img')


    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    image_data = decrypt(encrypted_data, userProfile.password)

    if image_data is None:
        return None

    image = Image.frombytes(mode=mode, size=[width, height], data=image_data)

    image_file = io.BytesIO()
    image.save(image_file, format="PNG")
    img = base64.b64encode(image_file.getvalue()).decode('ascii')

    return img


def replace_image(url: str, filename: str, userProfile: UserProfile) -> Image:
    image_data = Image.open(requests.get(url, stream=True).raw)
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, '..', 'images', filename + '.img')

    remove_image(filename)

    encrypt(file_path, image_data.tobytes(), userProfile.password)

    return image_data



def remove_image(filename: str):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, '..', 'images', filename + '.img')

    if os.path.exists(file_path):
        os.remove(file_path)