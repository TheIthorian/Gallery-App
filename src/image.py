import base64
import io
import os
import uuid
import server
from PIL import Image
import requests

from user import UserProfile # remove
from encryption import decrypt, encrypt, generate_key

def addImage (inputs, userProfile: UserProfile):

    responsePayload = server.ResponsePayload()

    # Data Auths
    if not server.serverConnection.dataAuthorisation("UserGalleryId", userProfile.userId, inputs['GalleryId']):
        responsePayload.status = 401
        responsePayload.results[0] = {
            'Type': 'Warning',
            'Code': None,
            'Description': 'Data Authorisation Error: UserGalleryId'
        }

        return [2, None, 'Data Authorisation Error: UserGalleryId'] # remove

    if inputs['Image'] is None:
        inputs['Image'] = ""

    if inputs['URL'] is None:
        inputs['URL'] = ""

    if len(inputs['URL']) == 0:
        return [2, 
        None, 
        "Empty Image"]

    if inputs['PublicImageIndicator'] == 6:
        publicImageUserId = userProfile.userId
    else:
        publicImageUserId = None

    title = inputs['Title']
    url  = inputs['URL']
    garllery_id = inputs['GalleryId']

    filename = f"{uuid.uuid4().hex}"

    image_data = save_image_to_file(url, filename, userProfile)

    # Insert the image data           
    queryInputs = {
        'Title': title, 
        'URL':url, 
        'Path':filename,
        'Suffix':image_data.mode,
        'Width':image_data.size[0],
        'Height':image_data.size[1],
        'Status':1, 
        'GalleryId':garllery_id,
        'UserId':userProfile.userId,
        'AddedByUserId':userProfile.userId
    }
    # print(queryInputs)
    imageId = server.serverConnection.runInsertQuery("Image","ImageInsert", queryInputs)

    image = server.serverConnection.runQuery("Image","GetImage", {'ImageId':imageId})[0]

    responsePayload.messages.append( {  
        'GalleryId' : garllery_id,
        'ImageId': image['ImageId'],
        'Title': image['Title'], 
        'URL': image['URL'],
        'Image': '0'
    })
    

    return [
        0, 
        {   
            'GalleryId' : inputs['GalleryId'],
            'ImageId': image['ImageId'],
            'Title': image['Title'], 
            'URL': image['URL'],
            'Image': '0'
        }, 
        None]


def updateImage (inputs, userProfile):

    imageId = inputs['ImageId']

    # Data Auths
    if not server.serverConnection.dataAuthorisation("UserGalleryId", userProfile.userId, inputs['GalleryId']):
        return [2, None, 'Data Authorisation Error: UserGalleryId']

    if not server.serverConnection.dataAuthorisation("GalleryIdImageId", inputs['GalleryId'], imageId):
        return [2, None, 'Data Authorisation Error: GalleryIdImageId']

    if len(inputs['URL']) == 0:
        return [2, 
        None, 
        "Empty Image"]


    # Update the image data           
    queryInputs = {
        'ImageId':imageId, 
        'Title':inputs['Title'], 
        'URL':inputs['URL'],
        'UserId':userProfile.userId
    }
    server.serverConnection.runQuery("Image","ImageUpdate", queryInputs)

    image = server.serverConnection.runQuery("Image","GetImage", {'ImageId':imageId})[0]

    return [
        0, 
        {   
            'GalleryId' : inputs['GalleryId'],
            'ImageId': image['ImageId'],
            'Title': image['Title'], 
            'URL': image['URL'],
            'Image': '0'
        }, 
        None]


def getImages (galleryId, userProfile):

    if galleryId < 0:
        images = server.serverConnection.runQuery("Image","GetImages", {'UserId':userProfile.userId})
    
    else:
        images = server.serverConnection.runQuery("Image","GetGalleryImages", {'UserId':userProfile.userId, 'GalleryId': galleryId})

    output = []

    for image in images:
        output.append({
            'GalleryId' : galleryId,
            'ImageId': image['ImageId'],
            'Title': image['Title'], 
            'URL': image['URL'],
            'Image': get_image_from_file(image['Path'], userProfile, image['Suffix'], image['Width'], image['Height'])
        })

    return [
        0, 
        output, 
        None]


def removeImage (inputs, userProfile):

    galleryId = inputs['GalleryId']
    imageId = inputs['ImageId']
        
    if not server.serverConnection.dataAuthorisation('UserGalleryId', userProfile.userId, galleryId):
        return [2, None, 'Data Authorisation Error: UserGalleryId']

    if not server.serverConnection.dataAuthorisation('GalleryIdImageId', galleryId, imageId):
        return [2, None, 'Data Authorisation Error: GalleryIdImageId']


    queryInputs = {
            'UserId':userProfile.userId, 
            'GalleryId':galleryId,
            'ImageId':imageId
        }

    server.serverConnection.runQuery("Image", "DeleteImage", queryInputs)

    output = getImages(galleryId, userProfile)[1]

    return [
        0, 
        output, 
        None]       
         

def save_image_to_file(url: str, filename: str, userProfile: UserProfile) -> Image:
    image_data = Image.open(requests.get(url, stream=True).raw)


    key = generate_key(userProfile.password)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, '..', 'images', filename + '.img')
    encrypt(file_path, image_data.tobytes(), key)

    return image_data


def get_image_from_file(filename: str, userProfile: UserProfile, mode, width, height) -> base64:
    if (filename is None or filename == 'xx'):
        return None

    key = generate_key(userProfile.password)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, '..', 'images', filename + '.img')

    image_data = decrypt(file_path, key)


    if image_data is None:
        return None

    image = Image.frombytes(mode=mode, size=[width, height], data=image_data)

    image_file = io.BytesIO()
    image.save(image_file, format="PNG")
    img = base64.b64encode(image_file.getvalue()).decode('ascii')

    return img



def addGallery (inputs, userProfile):

    # Insert the gallery data           
    queryInputs = {
        'Title':inputs['Title'], 
        'UserId':userProfile.userId
    }

    server.serverConnection.runQuery("Image", "GalleryInsert", queryInputs)

    return getGallery({'GalleryId': -1}, userProfile)


def getGallery (inputs, userProfile):

    galleryId = inputs['GalleryId']

    if galleryId > 0 and not server.serverConnection.dataAuthorisation('UserGalleryId', userProfile.userId, galleryId):
        return [2, None, 'Data Authorisation Error: UserGalleryId']

    if galleryId < 0:
        gallerys = server.serverConnection.runQuery("Image", "GetAllGallery", {'UserId':userProfile.userId})
    
    else:
        gallerys = server.serverConnection.runQuery("Image", "GetGallery", 
            {
                'UserId':userProfile.userId, 
                'GalleryId':galleryId
            })

    output = []

    for gallery in gallerys:
        output.append({
            'GalleryId': gallery['GalleryId'],
            'Title': gallery['Title'],
            'ImageCount':gallery['ImageCount']
        })

    return [
        0, 
        output, 
        None]     


def updateGallery (inputs, userProfile):

    for data in inputs:

        galleryId = data['GalleryId']
    
        if not server.serverConnection.dataAuthorisation('UserGalleryId', userProfile.userId, galleryId):
            return [2, None, 'Data Authorisation Error: UserGalleryId']


    for data in inputs:

        title = data['Title'] 
        galleryId = data['GalleryId']

        server.serverConnection.runQuery("Image", "CustomUpdateGallery", 
            {
                'UserId':userProfile.userId, 
                'GalleryId':galleryId,
                'Title':title
            })

        output = getGallery({'GalleryId':-1}, userProfile)[1]

    return [
        0, 
        output, 
        None]           


def removeGallery (inputs, userProfile):

    for data in inputs:

        galleryId = data['GalleryId']
        
        if not server.serverConnection.dataAuthorisation('UserGalleryId', userProfile.userId, galleryId):
            return [2, None, 'Data Authorisation Error: UserGalleryId']


    for data in inputs:

        galleryId = data['GalleryId']

        inputs = {
                'UserId':userProfile.userId, 
                'GalleryId':galleryId
            }

        server.serverConnection.runQuery("Image", "DeleteGalleryImages", inputs)
        server.serverConnection.runQuery("Image", "DeleteGallery", inputs)

        output = getGallery({'GalleryId':-1}, userProfile)[1]
        print(output)

    return [
        0, 
        output, 
        None]       
