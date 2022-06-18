import httpHelper
from router.router import HTTPRoute, HTTPRouter

from auth import isAuthenticated, hasPermission

class testApp(HTTPRouter):

    def addInitRoutes(self):

        self.addRoute(HTTPRoute('login/', self.login))
        self.addRoute(HTTPRoute('permtest/', self.permTest))


    def login(self, request, start_response):

        status = '200 OK'
        start_response(status, [])
        return [b'Login OK']

    @isAuthenticated
    @hasPermission('CN=DUMMY_GROUP,CN=Users,DC=mitch,DC=zone')
    def permTest(self, request, start_response):
  
        return httpHelper.sendJSONResponse(start_response, {'permission' : 'OK'})


