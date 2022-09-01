import base64
from dataclasses import dataclass
import io
import os
import uuid
from PIL import Image
import requests
from config import mysql
import pymysql

from encryption import decrypt, encrypt, generate_key
from image import save_image_to_file

IMAGE_URL = 'https://pixeljoint.com/files/icons/small__r1485254581.png'
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
    image = Image.open(requests.get(IMAGE_URL, stream=True).raw)
    image_before.mode = image.mode
    image_before.size = image.size
    image_before.data = image.tobytes()

    key = generate_key(USER_PROFILE['password'])

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'test_encrypted' + '.img')
    encrypt(file_path, image_before.data, key)


def test_decrypt():
    key = generate_key(USER_PROFILE['password'])
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path,'test_encrypted' + '.img')
    
    image_data = decrypt(file_path, key)

    image = Image.frombytes(mode=image_before.mode, size=image_before.size, data=image_data)
    image_after.mode = image.mode
    image_after.size = image.size
    image_after.data = image.tobytes()

    image.save('test_decrypted.png')

    image_file = io.BytesIO()
    image.save(image_file, format="PNG")
    img = base64.b64encode(image_file.getvalue())
    print(img)


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


if __name__ == '__main__':
    # test_encrypt()
    # test_decrypt()

    save_all()





    