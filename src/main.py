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
    userProfile.constructUserProfile(16)

    images = [
        "https://i.redd.it/otemldrznwi61.jpg",
        "https://preview.redd.it/7muizx9esti61.jpg?width=960&crop=smart&auto=webp&s=f1639e342a21687d93aee2936b88d01ca0cd55b6",
        "https://i.redd.it/jt5690hzv2i61.jpg",
        "https://i.redd.it/p5mu2wn0obh61.jpg",
        "https://i.redd.it/zvo7sz7ztzg61.jpg",
        "https://i.redd.it/tmb9i6v5awg61.png",
        "https://i.redd.it/mk3dh1bu0yg61.jpg",
        "https://i.redd.it/o5e3cejdevf61.png",
        "https://i.redd.it/91xpdr3fb0f61.jpg",
        "https://i.redd.it/xwxjapwvaue61.png",
        "https://i.redd.it/9z7cmn5812e61.png",
        "https://i.redd.it/tdxzxuzwhxd61.jpg",
        "https://i.redd.it/65fxinnzlxc61.jpg",
        "https://i.redd.it/rjwv4me4rvc61.png",
        "https://i.redd.it/ndm8oo8gc0c61.jpg",
        "https://preview.redd.it/ytsvyio67ab61.jpg?width=1000&format=pjpg&auto=webp&s=f5dda07b1263b54112828a25a05016dc265b63ec",
        "https://i.redd.it/e0ea5qnkgoa61.jpg",
        "https://i.redd.it/dnzg7smmoiz51.jpg",
        "https://i.redd.it/4ea9zcm3mwt51.png",
        "https://i.redd.it/6xoyb7xi0cl51.jpg",
        "https://i.redd.it/7tqf8j00w5l51.png",
        "https://i.redd.it/vogfzqwe75j51.png",
        "https://i.redd.it/7bo50l4ly6f51.png",
        "https://i.redd.it/fgprg2jcfvd51.png",
        "https://i.redd.it/5wd0rxc4isb51.jpg",
        "https://i.redd.it/moptfzsietb51.jpg",
        "https://i.redd.it/k9jp0r46kh651.jpg",
        "https://i.redd.it/hsm1vtac1q151.jpg",
        "https://i.redd.it/38me4fusui151.png",
        "https://i.redd.it/gn1ak52d36151.png",
        "https://i.redd.it/z6y1vo6en2151.png",
        "https://i.redd.it/ztjg5gf10x051.png",
        "https://i.redd.it/rhofbq6nzkz41.png",
        "https://i.redd.it/jxx5qjqjoez41.png",
        "https://i.imgur.com/FgJTPcI.jpg",
        "https://i.redd.it/pll69z1yr7x41.png",
        "https://i.redd.it/zvaj5leewpl41.jpg",
        "https://i.redd.it/hnmx4leaxr541.jpg",
        "https://i.redd.it/5zyfk1aumce41.png",
        "https://i.redd.it/lnhxyxfv74q41.png",
        "https://i.redd.it/jiimpe6djqs41.png",
        "https://i.redd.it/vok0f83af8s41.png",
        "https://i.redd.it/7ev7kzrjjtm41.jpg",
        "https://i.redd.it/imr0lcbpjia41.png",
        "https://i.redd.it/3b47u8xclg041.png",
        "https://i.redd.it/8vnxf9p3ohs31.jpg",
        "https://i.redd.it/7us6kiey09v61.jpg",
        "https://preview.redd.it/qveizk9zb6u61.jpg?width=1708&format=pjpg&auto=webp&s=682cd9cbaa81bb568cca1fc38ae3cf0d75fa7450",
        "https://preview.redd.it/e0hzb9ezb6u61.jpg?width=1708&format=pjpg&auto=webp&s=20ba20b4c36eb389f0014d0ae957033f21e53a9c",
        "https://preview.redd.it/39rvbayyb6u61.jpg?width=1708&format=pjpg&auto=webp&s=2aa34836a717823c8a5cdc6b1befc09c56b845d2",
        "https://i.redd.it/uy5wj8adebr61.jpg",
        "https://preview.redd.it/ey7h05mo9rq61.jpg?width=1920&format=pjpg&auto=webp&s=00ff3619b70297db397f90b321297e6e9c4fabee",
        "https://preview.redd.it/8zdem2swvgq61.jpg?width=1884&format=pjpg&auto=webp&s=60c217e7008e79f10be6f86b91ac9c5b789935ee",
        "https://i.redd.it/tt3fkav2kdp61.jpg",
        "https://i.redd.it/s0wocfx315p61.jpg",
        "https://i.redd.it/iij32c14tlo61.jpg",
        "https://preview.redd.it/ymuezowzktn61.jpg?width=960&crop=smart&auto=webp&s=8b972c22ae351b47d0ca965d9d60d50a9d0b8e6c",
        "https://i.redd.it/m6axauqbd9m61.jpg",
        "https://preview.redd.it/zefds8lpfel61.jpg?width=960&crop=smart&auto=webp&s=a2916aecb34631e5a87a76822377eafd21152b5b",
        "https://i.redd.it/fmwnxcjtm0k61.jpg"
    ]

    n = 0
    for i in images:
        if n % 20 == 0:
            print(n)
        n+=1
        imageData = {
            'GalleryId': 94,
            'Title' : 'Mincraft ' + str(n),
            'Image' : None,
            'URL' : i,
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

        
