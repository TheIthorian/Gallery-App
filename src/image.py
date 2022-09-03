import uuid
from file_handler import get_image_from_file, remove_image, replace_image, save_image_to_file
import server

from user import UserProfile # remove

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
    imageId = server.serverConnection.runInsertQuery("Image","ImageInsert", queryInputs)

    image = server.serverConnection.runQuery("Image","GetImage", {'ImageId':imageId})[0]

    responsePayload.messages.append( {  
        'GalleryId' : garllery_id,
        'ImageId': image['ImageId'],
        'Title': image['Title'], 
        'URL': image['URL'],
        'Image': '0'
    })

    try:
        image_data = get_image_from_file(image['Path'], userProfile, image['Suffix'], image['Width'], image['Height'])
    except:
        image_data = None

    return [
        0, 
        {   
            'GalleryId' : inputs['GalleryId'],
            'ImageId': image['ImageId'],
            'Title': image['Title'], 
            'URL': image['URL'],
            'Image':image_data
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

    image = server.serverConnection.runQuery("Image","GetImage", {'ImageId':imageId})[0]

    image_data = replace_image(image['URL'], image['Path'], userProfile)

    # Update the image data           
    queryInputs = {
        'ImageId':imageId, 
        'Title':inputs['Title'], 
        'URL':inputs['URL'],
        'Suffix':image_data.mode,
        'Width':image_data.size[0],
        'Height':image_data.size[1],
        'UserId':userProfile.userId
    }
    server.serverConnection.runQuery("Image","ImageUpdate", queryInputs)

    return [
        0, 
        {   
            'GalleryId' : inputs['GalleryId'],
            'ImageId': image['ImageId'],
            'Title': image['Title'], 
            'URL': image['URL'],
            'Image': get_image_from_file(image['Path'], userProfile, image_data.mode, image_data.size[0], image_data.size[1])
        }, 
        None]


def getImages (galleryId, userProfile):

    if galleryId < 0:
        images = server.serverConnection.runQuery("Image","GetImages", {'UserId':userProfile.userId})
    
    else:
        images = server.serverConnection.runQuery("Image","GetGalleryImages", {'UserId':userProfile.userId, 'GalleryId': galleryId})

    output = []

    for image in images:

        try:
            print(f"get_image_from_file: [{image['ImageId']}] {image['Path']}")
            image_data = get_image_from_file(image['Path'], userProfile, image['Suffix'], image['Width'], image['Height'])
        except:
            image_data = None

        output.append({
            'GalleryId' : galleryId,
            'ImageId': image['ImageId'],
            'Title': image['Title'], 
            'URL': image['URL'],
            'Image': image_data
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


    image = server.serverConnection.runQuery("Image","GetImage", {'ImageId':imageId})[0]

    remove_image(image['Path'])

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
        None
    ]       



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
