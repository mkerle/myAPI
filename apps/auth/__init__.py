import json

from router.router import HTTPRoute, HTTPRouter
from helpers import httpHelper
from helpers.decorators import allowedHTTPMethods

from auth.ldapBackend import LDAPBackend
from jwt.jwt import JWTHelper

class LDAPAuthentication(HTTPRouter):

    def __init__(self):
        super().__init__()
        self.authenticator = LDAPBackend()

    def addInitRoutes(self):
        
        self.addRoute(HTTPRoute('login/', self.login))

    @allowedHTTPMethods(['OPTIONS', 'POST'])
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

