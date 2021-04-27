import server

from config import mysql # remove

def addImage (inputs, userProfile):

    # Data Auths
    if not server.serverConnection.dataAuthorisation("UserGalleryId", userProfile.userId, inputs['GalleryId']):
        return [2, None, 'Data Authorisation Error: UserGalleryId']

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

    # Save image to system and save path


    # Insert the image data           
    queryInputs = {
        'Title':inputs['Title'], 
        'URL':inputs['URL'], 
        'Path':'xx',  
        'Status':1, 
        'UserId':userProfile.userId,
        'AddedByUserId':userProfile.userId
    }
    imageId = server.serverConnection.runInsertQuery("Image","ImageInsert", queryInputs)

    # Link the image to the gallery
    queryInputs = {
        'GalleryId' : inputs['GalleryId'],
        'ImageId' : imageId,
        'UserId' : userProfile.userId
    }

    galleryImageId = server.serverConnection.runInsertQuery("Image", "GalleryImageInsert", queryInputs)


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
            'Image': '0' 
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

    server.serverConnection.runQuery("Image", "DeleteGalleryImagesForRemoveImage", queryInputs)
    server.serverConnection.runQuery("Image", "DeleteUnassignedImages", {})

    output = getImages(galleryId, userProfile)[1]

    return [
        0, 
        output, 
        None]       
         


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

        server.serverConnection.runQuery("Image", "DeleteGallery", inputs)
        server.serverConnection.runQuery("Image", "DeleteGalleryImages", inputs)
        server.serverConnection.runQuery("Image", "DeleteUnassignedImages", {})

        output = getGallery({'GalleryId':-1}, userProfile)[1]
        print(output)

    return [
        0, 
        output, 
        None]       
