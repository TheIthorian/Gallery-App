from dataclasses import dataclass
import uuid
from file_handler import get_image_from_file, remove_image, replace_image, save_image_to_file
import server
from typing import Type, TypeVar

from user import UserProfile

T = TypeVar('T', bound='Image')


@dataclass
class Image:
    id: int = None
    title: str = None
    url: str = None
    path: str = None
    mode: str = None
    original_width: int = None
    original_height: int = None
    width: int = None
    height: int = None
    status: int = None
    gallery_id: int = None
    user_id: int = None
    added_by: int = None

    image_data: any = None  # PIL.Image

    @classmethod
    def from_model(cls: Type[T], row) -> T:
        return cls(id=row['ImageId'],
                   title=row['Title'],
                   url=row['URL'],
                   path=row['Path'],
                   mode=row['Suffix'],
                   width=row['Width'],
                   height=row['Height'],
                   status=row['Status'],
                   gallery_id=row['GalleryId'])

    def insert(self, userProfile: UserProfile) -> int:
        queryInputs = {
            'Title': self.title,
            'URL': self.url,
            'Path': self.path,
            'Suffix': self.image_data.mode,
            'Width': self.image_data.size[0],
            'Height': self.image_data.size[1],
            'Status': 1,
            'GalleryId': self.gallery_id,
            'UserId': userProfile.userId,
            'AddedByUserId': userProfile.userId
        }
        image_id = server.serverConnection.runInsertQuery(
            "Image", "ImageInsert", queryInputs)

        self.id = image_id
        return image_id


def addImage(inputs, userProfile: UserProfile):
    responsePayload = server.ResponsePayload()

    # Data Auths
    if not server.serverConnection.dataAuthorisation("UserGalleryId", userProfile.userId, inputs['GalleryId']):
        responsePayload.status = 401
        responsePayload.results[0] = {
            'Type': 'Warning',
            'Code': None,
            'Description': 'Data Authorisation Error: UserGalleryId'
        }

        return [2, None, 'Data Authorisation Error: UserGalleryId']

    if inputs['Image'] is None:
        inputs['Image'] = ""

    if inputs['URL'] is None:
        inputs['URL'] = ""

    if len(inputs['URL']) == 0:
        return [2,
                None,
                "Empty Image"]

    image = Image()
    image.title = inputs['Title']
    image.url = inputs['URL']
    image.gallery_id = inputs['GalleryId']
    image.path = f"{uuid.uuid4().hex}"

    image.image_data = save_image_to_file(image.url, image.path, userProfile)

    # Insert the image data
    image.id = image.insert(userProfile)

    responsePayload.messages.append({
        'GalleryId': image.gallery_id,
        'ImageId': image.id,
        'Title': image.title,
        'URL': image.url,
        'Image': '0'
    })

    try:
        image_data = get_image_from_file(
            image.path, userProfile, image.mode, image.width, image.height)
    except:
        image_data = None

    return [
        0,
        {
            'GalleryId': image.gallery_id,
            'ImageId': image.id,
            'Title': image.title,
            'URL': image.url,
            'Image': image_data
        },
        None]


def updateImage(inputs, userProfile):
    new_image = Image(id=inputs['ImageId'],
                      title=inputs['Title'],
                      url=inputs['URL'],
                      gallery_id=inputs['GalleryId'])

    # Data Auths
    if not server.serverConnection.dataAuthorisation("UserGalleryId", userProfile.userId, new_image.gallery_id):
        return [2, None, 'Data Authorisation Error: UserGalleryId']

    if not server.serverConnection.dataAuthorisation("GalleryIdImageId", new_image.gallery_id, new_image.id):
        return [2, None, 'Data Authorisation Error: GalleryIdImageId']

    if len(new_image.url) == 0:
        return [2,
                None,
                "Empty Image"]

    existing_image = Image.from_model(server.serverConnection.runQuery(
        "Image", "GetImage", {'ImageId': new_image.id})[0])

    new_image.image_data = replace_image(
        new_image.url, existing_image.path, userProfile)

    # Update the image data
    queryInputs = {
        'ImageId': new_image.id,
        'Title': new_image.title,
        'URL': new_image.url,
        'Suffix': new_image.image_data.mode,
        'Width': new_image.image_data.size[0],
        'Height': new_image.image_data.size[1],
        'UserId': userProfile.userId
    }
    server.serverConnection.runQuery(
        "Image", "ImageUpdate", queryInputs)  # This is not working??

    return [
        0,
        {
            'GalleryId': new_image.gallery_id,
            'ImageId': new_image.id,
            'Title': new_image.title,
            'URL': new_image.url,
            'Image': get_image_from_file(
                new_image.path,
                userProfile,
                new_image.image_data.mode,
                new_image.image_data.size[0],
                new_image.image_data.size[1])
        },
        None]


def getImages(galleryId, userProfile):

    if galleryId < 0:
        images = server.serverConnection.runQuery(
            "Image", "GetImages", {'UserId': userProfile.userId})

    else:
        images = server.serverConnection.runQuery("Image", "GetGalleryImages", {
                                                  'UserId': userProfile.userId, 'GalleryId': galleryId})

    output = []

    for image in images:

        try:
            print(f"get_image_from_file: [{image['ImageId']}] {image['Path']}")
            image_data = get_image_from_file(
                image['Path'], userProfile, image['Suffix'], image['Width'], image['Height'])
        except:
            image_data = None

        output.append({
            'GalleryId': galleryId,
            'ImageId': image['ImageId'],
            'Title': image['Title'],
            'URL': image['URL'],
            'Image': image_data
        })

    return [
        0,
        output,
        None]


def removeImage(inputs, userProfile):

    galleryId = inputs['GalleryId']
    imageId = inputs['ImageId']

    if not server.serverConnection.dataAuthorisation('UserGalleryId', userProfile.userId, galleryId):
        return [2, None, 'Data Authorisation Error: UserGalleryId']

    if not server.serverConnection.dataAuthorisation('GalleryIdImageId', galleryId, imageId):
        return [2, None, 'Data Authorisation Error: GalleryIdImageId']

    image = server.serverConnection.runQuery(
        "Image", "GetImage", {'ImageId': imageId})[0]

    remove_image(image['Path'])

    queryInputs = {
        'UserId': userProfile.userId,
        'GalleryId': galleryId,
        'ImageId': imageId
    }

    server.serverConnection.runQuery("Image", "DeleteImage", queryInputs)

    output = getImages(galleryId, userProfile)[1]

    return [
        0,
        output,
        None
    ]


def addGallery(inputs, userProfile):

    # Insert the gallery data
    queryInputs = {
        'Title': inputs['Title'],
        'UserId': userProfile.userId
    }

    server.serverConnection.runQuery("Image", "GalleryInsert", queryInputs)

    return getGallery({'GalleryId': -1}, userProfile)


def getGallery(inputs, userProfile):

    galleryId = inputs['GalleryId']

    if galleryId > 0 and not server.serverConnection.dataAuthorisation('UserGalleryId', userProfile.userId, galleryId):
        return [2, None, 'Data Authorisation Error: UserGalleryId']

    if galleryId < 0:
        gallerys = server.serverConnection.runQuery(
            "Image", "GetAllGallery", {'UserId': userProfile.userId})

    else:
        gallerys = server.serverConnection.runQuery("Image", "GetGallery",
                                                    {
                                                        'UserId': userProfile.userId,
                                                        'GalleryId': galleryId
                                                    })

    output = []

    for gallery in gallerys:
        output.append({
            'GalleryId': gallery['GalleryId'],
            'Title': gallery['Title'],
            'ImageCount': gallery['ImageCount']
        })

    return [
        0,
        output,
        None]


def updateGallery(inputs, userProfile):

    for data in inputs:

        galleryId = data['GalleryId']

        if not server.serverConnection.dataAuthorisation('UserGalleryId', userProfile.userId, galleryId):
            return [2, None, 'Data Authorisation Error: UserGalleryId']

    for data in inputs:

        title = data['Title']
        galleryId = data['GalleryId']

        server.serverConnection.runQuery("Image", "CustomUpdateGallery",
                                         {
                                             'UserId': userProfile.userId,
                                             'GalleryId': galleryId,
                                             'Title': title
                                         })

        output = getGallery({'GalleryId': -1}, userProfile)[1]

    return [
        0,
        output,
        None]


def removeGallery(inputs, userProfile):

    for data in inputs:

        galleryId = data['GalleryId']

        if not server.serverConnection.dataAuthorisation('UserGalleryId', userProfile.userId, galleryId):
            return [2, None, 'Data Authorisation Error: UserGalleryId']

    for data in inputs:

        galleryId = data['GalleryId']

        inputs = {
            'UserId': userProfile.userId,
            'GalleryId': galleryId
        }

        server.serverConnection.runQuery(
            "Image", "DeleteGalleryImages", inputs)
        server.serverConnection.runQuery("Image", "DeleteGallery", inputs)

        output = getGallery({'GalleryId': -1}, userProfile)[1]
        print(output)

    return [
        0,
        output,
        None]
