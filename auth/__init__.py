import json

from router.router import HTTPRoute, HTTPRouter
import httpHelper

from auth.ldapBackend import LDAPBackend
from jwt.jwt import JWTHelper

def isAuthenticated(func):

    def isAuthenticatedWrapper(self, request, start_response):
        user = request.get('USER', None)
        if (user and user.isAuthenticated()):
            return func(self, request, start_response)
        else:
            return httpHelper.send401Response(request, start_response)

    return isAuthenticatedWrapper

def hasPermission(group):

    def checkPermission(func):

        def checkPermissionWrapper(self, request, start_response):
            user = request.get('USER', None)
            if (user and group in user.groups):
                return func(self, request, start_response)
            else:
                return httpHelper.send401Response(request, start_response)

        return checkPermissionWrapper

    return checkPermission


class LDAPAuthentication(HTTPRouter):

    def __init__(self):
        super().__init__()
        self.authenticator = LDAPBackend()

    def addInitRoutes(self):
        
        self.addRoute(HTTPRoute('login/', self.login))

    
    def login(self, request, start_response):

        credentials = {}
        try:
            credentials = httpHelper.getJSONRequestBody(request)
        except:
            print('Could not get creds from request')
            return httpHelper.send400Response(request, start_response)

        try:
            user = self.authenticator.authenticate(credentials['username'], credentials['password'])

            if (user is not None):

                return httpHelper.sendJSONResponse(start_response, {'result' : 'OK', 'token' : JWTHelper.generateJWT(user.username, user.name, user.groups)})

            else:
                
                return httpHelper.sendJSONResponse(start_response, {'result' : 'login failed'})

        except Exception as e:
            print(e)
            return httpHelper.send400Response(request, start_response)            

