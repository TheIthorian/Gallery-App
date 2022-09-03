import base64
from dataclasses import dataclass
import io
import os
import uuid
from PIL import Image
import requests
from config import mysql
import pymysql

from encryption import decrypt, decrypt_xor, encrypt, encrypt_xor
from file_handler import get_image_from_file, rescale_image
from image import save_image_to_file

IMAGE_URL = 'https://pixeljoint.com/files/icons/small__r1485254581.png'
LARGE_IMAGE_URL = 'https://www.northlight-images.co.uk/wp-content/uploads/2015/05/pan_h_002336_lake-20x53p.jpg'

USER_PROFILE = {
    'password': 'password'
}

class Img:
    mode: str
    size: tuple[int, int]
    data: bytes
    
image_before = Img()
image_after = Img()

def test_encrypt():
    large_image = Image.open(requests.get(LARGE_IMAGE_URL, stream=True).raw)
    image = rescale_image(large_image)
    image_before.mode = image.mode
    image_before.size = image.size
    image_before.data = image.tobytes()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path,'test_encrypted' + '.img')

    ecnrypted_data = encrypt(image.tobytes(), USER_PROFILE['password'])
    with open(file_path, "xb") as file:
        file.write(ecnrypted_data)


def test_decrypt():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path,'test_encrypted' + '.img')
    
    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    image_data = decrypt(encrypted_data, USER_PROFILE['password'])

    image = Image.frombytes(mode=image_before.mode, size=image_before.size, data=image_data)
    image_after.mode = image.mode
    image_after.size = image.size
    image_after.data = image.tobytes()

    image.save('test_decrypted.png')

    image_file = io.BytesIO()
    image.save(image_file, format="PNG")
    img = base64.b64encode(image_file.getvalue())


def save_image(image_row):
    filename = f"{uuid.uuid4().hex}"

    @dataclass
    class Profile:
        password = image_row['Password']

    try:
        image = save_image_to_file(image_row['URL'], filename, Profile())
    except:
        return

    query = f"UPDATE Image SET Path = '{filename}', Suffix = '{image.mode}', Width = {image.size[0]}, Height = {image.size[1]} WHERE ImageId = {image_row['ImageId']}"
    print(query)
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()


def save_all():
    query = '''SELECT I.ImageId, I.URL, I.Path, U.UserId, U.username, U.password
    FROM Image I JOIN Users U on U.UserId = I.userId 
    WHERE I.path = "xx"
    ORDER BY U.UserId, I.ImageId'''

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    all_images = result

    for image in all_images:
        save_image(image)


def change_encryption():
    query = '''SELECT I.ImageId, I.URL, I.Path, I.Suffix, I.Width, I.Height, U.UserId, U.username, U.Password
    FROM Image I JOIN Users U on U.UserId = I.userId 
    ORDER BY U.UserId, I.ImageId'''

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    all_images = result

    class UserProfile:
        def __init__(self, password):
            self.password = password

    for image in all_images:
        print(image)
        try:
            save_image_to_file(image['URL'], image['Path'], UserProfile(image['Password']))
        except:
            continue


if __name__ == '__main__':
    # test_encrypt()
    # test_decrypt()

    # save_all()

    # change_encryption()
