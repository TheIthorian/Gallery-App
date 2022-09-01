import pymysql
import server

from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
import hashlib, uuid

import re



class UserProfile ():

    def __init__(self):

        self.email = None
        self.userId = None
        self.authenticated = False
        self.password = None
        self.admin = False

    
    def constructUserProfile(self, userId):

        if userId > 0:
            result = server.serverConnection.runQuery("User", "GetUserSecurityProfile", {'UserId':userId})

            if len(result) > 0:
                result = result[0]
                self.email = result['Email']
                self.userId = result['UserId']
                self.username = result['Username']
                self.emaAuthenticated = True
                self.password = result['HashedPassword']
                if result['AdminInd'] == 6: self.admin = True
            else:
                raise ValueError('Could not find the user security profile')

        else: 
            self.email = 'DummyEmail'
            self.userId = -1
            self.username = "DummyUsername"
            self.emaAuthenticated = True
            self.password = None
            self.admin = False


    #def __del__(self):

    def authenticateUser(self, sessionId, username, password):
        verified = False

        if sessionId is None and username is None and password is None: # User Password
            #jsonify({"message":"Error: Unable to log in. No password / sessionId given"})
            return False

        if sessionId is not None:
            verified = self.sessionLogin(sessionId)
            
        if username is not None and password is not None and not verified:
            verified = self.userLogin(username, password, None)['verified']

        return verified


    def isEmailValid(self, email):
        valid = True

        if len(email) < 3:
            valid = False
        
        return valid


    def isPasswordValid(self, password):
        valid = True

        if len(password) > 32 or len(password) < 5:
            valid = False

        return valid


    # Create a new session for the user, given the client sessionId
    def registerSession(self, sessionId):
        # UPDTAE: Should check if the session already exists first
        try:
            inputs = {'SessionID':sessionId, 'UserId':self.userId, 'UserId2':self.userId}
            server.serverConnection.runQuery("User", "CreateUserSession", inputs)
        except Exception as e:
            print(e)
            return 'Error: ' + str(e)


    def sessionLogin(self, sessionId):
        try:
            result = server.serverConnection.runQuery("User", "GetUserSession", {'SessionID':sessionId})

        except Exception as e:
            print(e)
            return 'Error: ' + str(e)


        if len(result) > 0:
            result = result[0]
            # Resgistration succeeded
            self.email = result['Email']
            self.userId = result['UserId']
            self.username = result['Username']
            self.emaAuthenticated = True
            if result['AdminInd'] == 6: self.admin = True

            return True

        # Authentication failed
        return False


    def userLogin(self, username, password, sessionId):

        username = username.strip()
        password = password.strip()

        if not self.isPasswordValid(password):
            return {
                'verified' : False,
                'error' : "Invalid credentials"
            }
        
        try:    
            result = server.serverConnection.runQuery("User", "ValidatePasswordForUser", {'Username':username})
        except Exception as e:
            return {
                'verified' : False,
                'error' : "Unexpected error. Please try again."
            }

        if len(result) == 0:
            return {
                'verified' : False,
                'error' : "Invalid credentials"
            }

        result = result[0]

        hash = hashlib.sha512()
        passwordSalt = result['PasswordSalt']
        hash.update(('%s%s' % (passwordSalt, password)).encode('utf-8'))
        password_hash = hash.hexdigest()

        if password_hash == result['Password']:
            self.userId = result['UserId']
            self.email = result['Email']
            self.username = result['Username']
            self.authenticated = True
            if result['AdminInd'] == 6: self.admin = True
        else:
            return {
                'verified' : False,
                'error' : "Invalid credentials"
            }

        sessionId = -1 if sessionId is None else sessionId
        self.registerSession(sessionId)
        
        return {
                'verified' : True,
                'error' : ""
            }


    def userLogout(self):
        print("Entering Logout")
        print(self.userId)

        try:    
            server.serverConnection.runQuery("User", "DeleteUserSession", {'UserId':self.userId})
        except:
            print("SQL Error")
            return False

        self.authenticated = False
        del self
        return True



@app.route('/registerUserSession/<int:sessionId>', methods=['POST'])
def registerUserSession(sessionId):
    userProfile = UserProfile()
    result = userProfile.registerSession(sessionId)
    return result

        
def register(email, username, password, sessionId):
    
    minPasswordLength = 5
    minUsernameLength = 1

    # Password validations
    # Legnth
    if len(password) < minPasswordLength:
        return [2, None, "Password must be at least 5 characters"]

    # Email validations
    # Regex
    if not re.search("[^@]+@[^@]+\.[^@]+", email) and len(email) > 0:
        print(email)
        return [2, None, "Invalid Email"]

    # Exists
    if len(email) > 0:
        result = server.serverConnection.runQuery("User", "EmailExists", {'Email':email})
        if len(result) > 0:
            return [2, None, "Email already exists"]


    # Username validations
    # Length
    if len(username) < minUsernameLength:
        return [2, None, "Invalid Username"]

    # Exists
    result = server.serverConnection.runQuery("User", "UsernameExists", {'Username':username})
    if len(result) > 0:
        return [2, None, "Username already exists"]
        

    try:
        hash = hashlib.sha512()
        passwordSalt = uuid.uuid4().hex
        hash.update(('%s%s' % (passwordSalt, password)).encode('utf-8'))
        passwordHash = hash.hexdigest()
        
        inputs = {'Username':username, 
        'Email':email if len(email) > 0 else None, 
        'Password':passwordHash, 
        'PasswordSalt':passwordSalt,
        'AdminInd':5,
        'Status':1}

        userId = server.serverConnection.runInsertQuery("User","UsrInsert", inputs)

        # Register the session
        userProfile = UserProfile()
        userProfile.constructUserProfile(userId)
        userProfile.registerSession(sessionId)

        return [
            0, 
            {
                'UserId': userId,
                'Username':username, 
                'Email':email
            }, 
            None]
        

    except Exception as e:
        print(e)
        return [3, None, 'Unknown Error']

