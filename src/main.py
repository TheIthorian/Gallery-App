#---------------------
# Component: main.py
# Description: Communication between web and Backend
#---------------------

"""
Todo:

"""

from app import app
from flask import jsonify, request
from flask import jsonify, flash, request, g

# App components
import user
import image

# Functional libraries
import base64
from datetime import datetime


if __name__  == "__main__":
    app.debug = True
    app.config['CORS_HEADERS'] = 'Content-Type'

    


# Output[0] = Result Type
  # 0: Success
  # 1: Info
  # 2: Warning
  # 3: Internal Error
# Output[1] = Message
# Output[2] = Error Message
def formatOutput(output):

    # Warning
    if output[0] == 3:
        return jsonify({
            'Result':output[2],
            'InternalError':True
        })
    if output[0] == 2:
        return jsonify({
            'Result':output[2]
        })
    # Info
    elif output[0] == 1:
        return jsonify({
            'Message':output[1],
            'Result':output[2]
            })
    # Success
    else:
        return jsonify({
            'Message':output[1],
            'Result':'Success'
            })


def formatOutputs(outputs):

    message = []

    for output in outputs:
        # Warning
        if output[0] == 3:

            message.append({
                'Result':output[2],
                'InternalError':True
            })
        if output[0] == 2:
            message.append({
                'Result':output[2]
            })
        # Info
        elif output[0] == 1:
            message.append({
                'Message':output[1],
                'Result':output[2]
                })
        # Success
        else:
            message.append({
                'Message':output[1],
                'Result':'Success'
                })

    return jsonify(message)


def printRequest(request):

    try:
        print("\n\n------------------------------------------------\n")
        print("Request:\t", request.url, request.method)
        print("Endpoint:\t", request.endpoint)
        print("Time:\t" + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

        print("Args: ")
        for key, value in request.args.items():
            print(key, ":", value)

        if request.json is not None or request.data == "b''":
            print("Data: ", request.data)
            for key, value in request.json.items():
                print("\t", key, ":", value)
        else:
            print("Data: None")

        print("Headers: ")
        for header in request.headers:
            print("\t", header)
    except (KeyError, AttributeError) as e:
        print("unable to print data: ", str(e))

    try:
        print("Authorization: ", request.authorization.username, request.authorization.password)
    except Exception as e:
        print("No authorisation present: ", str(e))


def printResponse(response):
    try:
        print("\nresponse")
        print("Time:\t" + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        if response.json is not None or response.data == "b''":
            print("Data: ", response.data)
            for key, value in response.json.items():
                print("\t", key, ":", value)
        else:
            print("Data: None")

        print("Headers: ")
        for header in response.headers:
            print("\t", header)
    except (KeyError, AttributeError) as e:
        print("unable to print data: ", str(e))




# Called before request is processed
@app.before_request
def before_request_callback():

    #if request.method == "OPTIONS":
        #return

    g.userId = -1
    
    printData = False
    #printData = True

    if request.endpoint in app.view_functions and request.method != 'OPTIONS':
        view_func = app.view_functions[request.endpoint]

        # Print request data
        if app.debug and request.method != 'OPTIONS' and printData:
            printRequest(request)
            app.logger.debug('EndPoint: %s', request.endpoint)
            app.logger.debug('Headers: %s', request.headers)
            app.logger.debug('Body: %s', request.get_data())
            

        # Authenticate user details
        if not hasattr(view_func, '_excludeUserAuthentication'): # Ingore methods that can be done without user auth
            
            sessionId = None if request.headers.get('sessionId') is None else request.headers.get('sessionId')

            if request.authorization:
                username = None if request.authorization.username is None else request.authorization.username
                password = None if request.authorization.password is None else request.authorization.password
            else:
                username = None
                password = None

            # Initialise user profile
            userProfile = user.UserProfile()
            verified = userProfile.authenticateUser(sessionId, username, password)
            if not verified:
                return jsonify({'Error':'Unable to authenticate user'})

            g.userId = userProfile.userId

                                                                                   
# Called before response is output to web service. Formats BE outputs
@app.after_request
def after_request(response):
    #printResponse(response)

    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers['Access-Control-Allow-Request-Headers'] = '*'
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, HEAD, OPTIONS, POST, PUT, DELETE"
    response.headers.add('Access-Control-Allow-Headers', 'Access-Control-Allow-Headers')
    response.headers.add('Access-Control-Allow-Headers', 'Origin')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Headers', 'Access-Control-Request-Method')
    response.headers.add('Access-Control-Allow-Headers', 'Access-Control-Request-Headers')
    response.headers.add('Access-Control-Allow-Headers', 'Accept')
    response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
    response.headers.add('Access-Control-Allow-Headers', 'sessionId')
    response.headers.add('Access-Control-Allow-Headers', 'password')
    response.headers.add('Access-Control-Allow-Headers', 'username')
    response.headers.add('Access-Control-Allow-Headers', 'status')
    response.headers.add('Access-Control-Allow-Headers', 'authorization')

    #response.headers["Access-Control-Allow-Headers"] = ["Access-Control-Allow-Headers", "Origin", "Content-Type", "Access-Control-Request-Method", "Access-Control-Request-Headers", 
    #"Accept", "X-Requested-With", "sessionId", "password", "username", "status", "authorization"]
    
    #esponse.headers['X-Content-Type-Options'] = 'nosniff'

    return response





################################################
# Decorators
################################################
# Decorator to exclude authentication. Unregistered users can run these calls.
def excludeUserAuthentication(function):
    function._excludeUserAuthentication = True
    return function



################################################
# Debug function
################################################
@app.route('/Debug/<int:repeats>', methods=["POST"])
@excludeUserAuthentication
def debug (repeats):
    return ({'Message':None})

    userProfile = userProfile = user.UserProfile()    
    userProfile.constructUserProfile(5)

    n = repeats
    for i in range(0, n):
        if i % 20 == 0:
            print(i)
        imageData = {
            'GalleryId': 91,
            'Title' : 'Test Image: ' + str(i),
            'Image' : None,
            'URL' : 'https://s.yimg.com/ny/api/res/1.2/1ziUOraUowhjKxJMC09kaA--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTk2MA--/https://s.yimg.com/uu/api/res/1.2/B9piw3Vtqdx71mEmaB7Z5g--~B/aD0xNzMyO3c9MTczMjthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/hearst_prevention_66/78d81e741dc89f64ad6ba3be2d50e7d' + str(i),
            'PublicImageIndicator' : 5
        }
        image.addImage(imageData, userProfile)

    return ({'Message': 'Successfully added ' + str(n) + ' images'})




################################################
# User functions
################################################
#  Register
#  Login
#  Logout

# Creates a new user
@app.route('/Register', methods=["POST"])
@excludeUserAuthentication
def _register():

    requestSchema = request.json
    email = requestSchema['Email'].strip()
    username = requestSchema['Email'].strip()
    password = requestSchema['Password'].strip()

    sessionId = None if request.headers.get('sessionId') is None else request.headers.get('sessionId')

    # Register the user
    output = user.register(email, username, password, sessionId)

    output = formatOutput(output)

    return output


# Retuns sessionId for FE
@app.route('/Login', methods=["POST"])
@excludeUserAuthentication
def _login():

    userProfile = user.UserProfile()

    requestSchema = request.json
    email = requestSchema['Email'].strip()
    username = requestSchema['Email'].strip()
    password = requestSchema['Password'].strip()
    sessionId = request.headers.get('sessionId')

    loginResult = userProfile.userLogin(username, password, sessionId)

    if not loginResult['verified']:
        return formatOutput([2, None, loginResult['error']])
    
    # SessionId saved to DB

    output = [0, sessionId, None]

    output = formatOutput(output)
    
    return output



@app.route('/Logout', methods=["POST"])
@excludeUserAuthentication
def _logout():

    userProfile = user.UserProfile()
    
    sessionId = request.headers.get('sessionId')
    userProfile.sessionLogin(sessionId)

    if not userProfile.userLogout():
        return formatOutput([2, None, 'Unable to log out'])
    
    output = [0, 'Logout succesful', None]

    output = formatOutput(output)
    
    return output





################################################
# Gallery Functions
################################################
# AddImage
# GetImages
# AddGallery
# GetGallery

#---------------
# Images

@app.route('/Gallery/<int:galleryId>/AddImage', methods=["POST"])
def _addImage(galleryId):
    userProfile = user.UserProfile()    
    userProfile.constructUserProfile(int(g.userId))

    requestData = request.json

    # Validate inputs - should use open source for this
    """fields = ['Title', 'URL', 'Image', 'PublicImageIndicator']

    for field in fields:
        if field not in requestData:
            return formatOutput([3, None, 'Schema Error: Missing ' + field])"""

    inputs = {
        'GalleryId': galleryId,
        'Title': requestData['Title'],
        'URL': requestData['URL'],
        'Image': requestData['Image'],
        'PublicImageIndicator': requestData['PublicImageIndicator']
    }
    
    output = image.addImage(inputs, userProfile)
        
    return formatOutput(output)


@app.route('/Gallery/<int:galleryId>/Image/<int:imageId>/Update', methods=["POST"])
def _updateImage(galleryId, imageId):
    userProfile = user.UserProfile()    
    userProfile.constructUserProfile(int(g.userId))

    requestData = request.json

    inputs = {
        'GalleryId': galleryId,
        'ImageId': imageId,
        'Title': requestData['Title'],
        'URL': requestData['URL']
    }
    
    output = image.updateImage(inputs, userProfile)
    
    return formatOutput(output)



@app.route('/GetImages', methods=["GET"])
@app.route('/Gallery/<int:galleryId>/Images', methods=["GET"])
def _getImages(galleryId = -1):

    if g.userId is None:
        return formatOutput([3, None, 'Unable to authenticate user'])

    userProfile = user.UserProfile()    
    userProfile.constructUserProfile(int(g.userId))

    output = image.getImages(galleryId, userProfile)
    return formatOutput(output)


@app.route('/Gallery/<int:galleryId>/RemoveImage/<int:imageId>', methods=["DELETE"])
def _removeImage(galleryId, imageId):

    if g.userId is None:
        return formatOutput([3, None, 'Unable to authenticate user'])

    userProfile = user.UserProfile()    
    userProfile.constructUserProfile(int(g.userId))    

    inputs = {
        'ImageId':imageId,
        'GalleryId':galleryId
    }

    output = image.removeImage(inputs, userProfile)

    return formatOutput(output)

#----------------



#----------------
# Gallery

@app.route('/AddGallery', methods=["POST"])
def _addGallery():
    userProfile = user.UserProfile()    
    userProfile.constructUserProfile(int(g.userId))

    requestData = request.json

    # Validate inputs - should use open source for this
    if len(requestData['Title']) > 45:
        return [0, None, 'Title must be less than 45 characters']

    inputs = {'Title': requestData['Title']}
    
    output = image.addGallery(inputs, userProfile)
        
    return formatOutput(output)


@app.route('/GetGallery/', methods=["GET"])
@app.route('/GetGallery/<int:galleryId>', methods=["GET"])
def _getGallery(galleryId = -1):

    if g.userId is None:
        return formatOutput([3, None, 'Unable to authenticate user'])

    userProfile = user.UserProfile()    
    userProfile.constructUserProfile(int(g.userId))    

    output = image.getGallery({'GalleryId':galleryId}, userProfile)

    return formatOutput(output)


@app.route('/UpdateGallery/', methods=["POST"])
@app.route('/UpdateGallery/<int:galleryId>', methods=["POST"])
def _updateGallery(galleryId = -1):

    if g.userId is None:
        return formatOutput([3, None, 'Unable to authenticate user'])

    userProfile = user.UserProfile()    
    userProfile.constructUserProfile(int(g.userId))    

    requestData = request.json

    inputs = []
    if galleryId < 0:
        
        for message in requestData['Message']:
            inputs.append({
                'GalleryId' : message['GalleryId'],
                'Title' : message['Title']
            })
    else:
        inputs.append({
            'GalleryId' : galleryId,
            'Title' : requestData['Title']
        })

    output = image.updateGallery(inputs, userProfile)

    return formatOutput(output)


@app.route('/RemoveGallery/', methods=["POST"])
@app.route('/RemoveGallery/<int:galleryId>', methods=["POST"])
def _removeGallery(galleryId = -1):

    if g.userId is None:
        return formatOutput([3, None, 'Unable to authenticate user'])

    userProfile = user.UserProfile()    
    userProfile.constructUserProfile(int(g.userId))    

    requestData = request.json

    inputs = []
    if galleryId < 0:
        
        for message in requestData:
            inputs.append({
                'GalleryId' : message['GalleryId']
            })
    else:
        inputs.append({
            'GalleryId' : galleryId
        })

    output = image.removeGallery(inputs, userProfile)

    return formatOutput(output)

#----------------






@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()

        
