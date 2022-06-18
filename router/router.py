
import re
import types
import sys
import httpHelper

class HTTPRoute():

    def __init__(self, path, handler):

        if (path[0] == '/'):
            self.path = r'^%s.*' % (path)
        else:
            self.path = r'.*%s.*' % (path)

        self.handler = handler

    def matchPath(self, requestPath):

        match = re.search(self.path, requestPath)
        return match is not None

    def processRequest(self, request, start_response):

        if (type(self.handler) == types.FunctionType or type(self.handler) == types.MethodType):
            return self.handler(request, start_response)
        elif (isinstance(self.handler, HTTPRouter)):
            return self.handler.processRequest(request, start_response)

        raise ValueError(self.handler)

class HTTPRouter():

    def __init__(self):
        self.routes = []
        self.addInitRoutes()

    def addInitRoutes(self):
        pass

    def addRoute(self, route):

        self.routes.append(route)

    def processRequest(self, request, start_response):

        for route in self.routes:
            print('Checking for match: %s and %s' % (route.path, request['PATH_INFO']))
            if (route.matchPath(request['PATH_INFO'])):
                print('Found match for match: %s and %s' % (route.path, request['PATH_INFO']))
                return route.processRequest(request, start_response)

        return httpHelper.send404Response(request, start_response)
                

        

